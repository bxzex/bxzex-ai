# BXZEX Uncensored AI · the model on a graphics card in your own Modal account
# Copyright (c) 2026 bxzex. All rights reserved. · https://bxzex.com · instagram.com/bxzex
# Free to use. Not to be copied, modified, rebranded or redistributed. See LICENSE.
#
# /cloud in bxzex-ai does all of this for you. By hand it is:
#   modal secret create bxzex-gpu ENGINE_KEY=<any long random text>
#   modal run cloud.py::fetch      copies the model into your Modal account, once (about 23GB, or 120GB for the bigger one on the H200)
#   modal deploy cloud.py          puts it online and prints its address
# then "remote" (that address) and "remote_key" (the same random text) in ~/.bxzex-ai/config.json.
import os, subprocess
import modal

GPU = "H100"              # or A100-80GB or L40S: a bit slower, and they cost less per hour. H200 runs the bigger model
BIG = GPU == "H200"       # the bigger, sharper model only fits on the H200's 141GB
IDLE_SECONDS = 60         # the card switches off this long after the last request, and Modal stops billing
CTX = 65536 if GPU in ("L40S", "H200") else 131072     # less memory to spare on these, so they hold a shorter chat

app = modal.App("bxzex-ai-gpu")
models = modal.Volume.from_name("bxzex-gpu-models", create_if_missing=True)

if BIG:
    WEIGHTS = "mradermacher/Qwen3.8-Flash-Next-Uncensored-GGUF"
    MODEL = "Qwen3.8-Flash-Next-Uncensored.Q4_K_M.gguf"
    PARTS = [f"{MODEL}.part{i}of3" for i in (1, 2, 3)]      # it comes as three plain pieces of one file, joined after the download
    VISION = "Qwen3.8-Flash-Next-Uncensored.mmproj-f16.gguf"
    FAST_DRAFT = []                                         # this build has no draft layers to speed it up, and doesn't need them
else:
    # Qwopus 3.8 27B Flash V2, uncensored: sharpest 27B for code and agent work, thinks less than the plain 27B
    WEIGHTS = "mradermacher/Qwopus3.8-27B-Flash-V2-abliterated-GGUF"
    MODEL = "Qwopus3.8-27B-Flash-V2-abliterated.Q6_K.gguf"
    PARTS = []
    VISION = "Qwopus3.8-27B-Flash-V2-abliterated.mmproj-f16.gguf"
    FAST_DRAFT = []                                         # this build has no draft layers (the engine exits if asked to use them)

# pinned: newer engine builds read prompts far slower on these cards
image = modal.Image.from_registry("ghcr.io/ggml-org/llama.cpp:server-cuda-b11382", add_python="3.12").entrypoint([])


@app.function(image=modal.Image.debian_slim().pip_install("huggingface_hub[hf_transfer]").env({"HF_HUB_ENABLE_HF_TRANSFER": "1"}),
              volumes={"/models": models}, timeout=4 * 3600, cpu=8)
def fetch():
    from huggingface_hub import hf_hub_download
    for name in (VISION,) if PARTS else (MODEL, VISION):
        if os.path.exists(f"/models/{name}"): print("already there:", name); continue
        print(hf_hub_download(WEIGHTS, name, local_dir="/models"))
    if PARTS and os.path.exists(f"/models/{MODEL}"): print("already there:", MODEL)
    elif PARTS:
        for name in PARTS: print(hf_hub_download(WEIGHTS, name, local_dir="/tmp/parts"))
        with open(f"/models/{MODEL}.joining", "wb") as out:
            for name in PARTS:
                with open(f"/tmp/parts/{name}", "rb") as f:
                    while True:
                        block = f.read(64 << 20)
                        if not block: break
                        out.write(block)
        os.rename(f"/models/{MODEL}.joining", f"/models/{MODEL}")
        print("joined:", MODEL)
    models.commit()


def fast_copy(src, dst, chunk=256 << 20):
    """Copy with 32 readers at once: one plain cp off the volume runs at ~0.15 GB/s on a fresh card, this at ~2.5 GB/s."""
    from concurrent.futures import ThreadPoolExecutor
    size = os.path.getsize(src)
    with open(dst, "wb") as f: f.truncate(size)
    def part(off):
        fi, fo = os.open(src, os.O_RDONLY), os.open(dst, os.O_WRONLY)
        try:
            pos, end = off, min(off + chunk, size)
            while pos < end:
                b = os.pread(fi, min(16 << 20, end - pos), pos)
                if not b: raise IOError(f"short read at {pos}")
                os.pwrite(fo, b, pos); pos += len(b)
        finally: os.close(fi); os.close(fo)
    with ThreadPoolExecutor(32) as ex: list(ex.map(part, range(0, size, chunk)))


# 4 requests at once (the chat, helpers side by side, the background learner) sharing one memory pool
@app.function(image=image, gpu=GPU, cpu=8 if BIG else 4, memory=32768 if BIG else 16384, volumes={"/models": models},
              secrets=[modal.Secret.from_name("bxzex-gpu")], scaledown_window=IDLE_SECONDS,
              timeout=3600, max_containers=1)
@modal.concurrent(max_inputs=8)
@modal.web_server(port=8080, startup_timeout=1500 if BIG else 600)
def engine():
    # copy the model onto the card's own disk first: read straight off the network volume it runs at 1 tok/s
    import time; t0 = time.time()
    for f in (MODEL, VISION): fast_copy(f"/models/{f}", f"/tmp/{f}")
    print(f"copied in {time.time() - t0:.0f}s")
    # the card builds its own code the first time it runs the model (60-90 s of paid, near-idle time on every wake);
    # keep what it built on the volume so later wakes reuse it
    os.makedirs("/models/cuda-cache", exist_ok=True)
    os.environ.update(CUDA_CACHE_PATH="/models/cuda-cache", CUDA_CACHE_MAXSIZE=str(4 << 30), CUDA_CACHE_DISABLE="0")
    proc = subprocess.Popen([
        "/app/llama-server", "--model", f"/tmp/{MODEL}", "--mmproj", f"/tmp/{VISION}",
        "--alias", "bxzex-uncensored", "--host", "0.0.0.0", "--port", "8080",
        "--api-key", os.environ["ENGINE_KEY"],
        "--ctx-size", str(CTX), "--parallel", "4", "--kv-unified", "--n-gpu-layers", "99", "--flash-attn", "on",
        "--cache-type-k", "q8_0", "--cache-type-v", "q8_0", "--batch-size", "2048", "--ubatch-size", "512",
        "--threads", "4", "--threads-batch", "4",
        *FAST_DRAFT,
        "--temp", "0.7", "--top-k", "20", "--top-p", "0.95", "--min-p", "0.0", "--repeat-penalty", "1.0",
        "--jinja"])
    # the very first request on a fresh card is slow (about 1 tok/s) while the engine sets itself up, so make it here
    import json, urllib.request
    key = {"Authorization": f"Bearer {os.environ['ENGINE_KEY']}", "Content-Type": "application/json"}
    for _ in range(1200 if BIG else 600):
        try:
            urllib.request.urlopen("http://127.0.0.1:8080/health", timeout=2); break
        except Exception:
            if proc.poll() is not None: raise SystemExit("engine stopped while starting")   # don't keep a paid card waiting on nothing
            time.sleep(1)
    print(f"engine up in {time.time() - t0:.0f}s")
    for words in ("hi", "Write two sentences about the sea.", "Sum this up in one line: " + "the tide comes in and the tide goes out. " * 300):
        body = json.dumps({"messages": [{"role": "user", "content": words}], "max_tokens": 32,
                           "chat_template_kwargs": {"enable_thinking": False}}).encode()
        try: urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:8080/v1/chat/completions", body, key), timeout=300).read()
        except Exception as e: print("warm-up:", e)
    print(f"warm in {time.time() - t0:.0f}s")
    try: models.commit()
    except Exception as e: print("cache save:", e)
