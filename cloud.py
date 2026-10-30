# BXZEX Uncensored AI · the model on a graphics card in your own Modal account
# Copyright (c) 2026 bxzex. All rights reserved. · https://bxzex.com · instagram.com/bxzex
# Free to use. Not to be copied, modified, rebranded or redistributed. See LICENSE.
#
# /cloud in bxzex-ai does all of this for you. By hand it is:
#   modal secret create bxzex-gpu ENGINE_KEY=<any long random text>
#   modal run cloud.py::fetch      copies the model into your Modal account, once (about 23GB)
#   modal deploy cloud.py          puts it online and prints its address
# then "remote" (that address) and "remote_key" (the same random text) in ~/.bxzex-ai/config.json.
import os, subprocess
import modal

GPU = "H100"              # or A100-80GB or L40S: a bit slower, and they cost less per hour
IDLE_SECONDS = 300        # the card switches off this long after the last request, and Modal stops billing
CTX = 65536 if GPU == "L40S" else 131072     # the L40S has less memory, so it holds a shorter chat

app = modal.App("bxzex-ai-gpu")
models = modal.Volume.from_name("bxzex-gpu-models", create_if_missing=True)

WEIGHTS = "bartowski/orcarouter_Qwen3.8-27B-Uncensored-GGUF"
MODEL = "orcarouter_Qwen3.8-27B-Uncensored-Q6_K.gguf"
VISION = "mmproj-orcarouter_Qwen3.8-27B-Uncensored-f16.gguf"

# pinned: newer engine builds read prompts far slower on these cards
image = modal.Image.from_registry("ghcr.io/ggml-org/llama.cpp:server-cuda-b11382", add_python="3.12").entrypoint([])


@app.function(image=modal.Image.debian_slim().pip_install("huggingface_hub[hf_transfer]").env({"HF_HUB_ENABLE_HF_TRANSFER": "1"}),
              volumes={"/models": models}, timeout=3600, cpu=4)
def fetch():
    from huggingface_hub import hf_hub_download
    for name in (MODEL, VISION):
        if os.path.exists(f"/models/{name}"): print("already there:", name); continue
        print(hf_hub_download(WEIGHTS, name, local_dir="/models"))
    models.commit()


# 4 requests at once (the chat, helpers side by side, the background learner) sharing one memory pool
@app.function(image=image, gpu=GPU, cpu=4, memory=16384, volumes={"/models": models},
              secrets=[modal.Secret.from_name("bxzex-gpu")], scaledown_window=IDLE_SECONDS,
              timeout=3600, max_containers=1)
@modal.concurrent(max_inputs=8)
@modal.web_server(port=8080, startup_timeout=600)
def engine():
    # copy the model onto the card's own disk first: read straight off the network volume it runs at 1 tok/s
    for f in (MODEL, VISION): subprocess.run(["cp", f"/models/{f}", f"/tmp/{f}"], check=True)
    subprocess.Popen([
        "/app/llama-server", "--model", f"/tmp/{MODEL}", "--mmproj", f"/tmp/{VISION}",
        "--alias", "bxzex-uncensored", "--host", "0.0.0.0", "--port", "8080",
        "--api-key", os.environ["ENGINE_KEY"],
        "--ctx-size", str(CTX), "--parallel", "4", "--kv-unified", "--n-gpu-layers", "99", "--flash-attn", "on",
        "--cache-type-k", "q8_0", "--cache-type-v", "q8_0", "--batch-size", "2048", "--ubatch-size", "512",
        "--threads", "4", "--threads-batch", "4",
        "--spec-type", "draft-mtp", "--spec-draft-n-max", "3", "--spec-draft-p-min", "0.4",
        "--temp", "0.7", "--top-k", "20", "--top-p", "0.95", "--min-p", "0.0", "--repeat-penalty", "1.0",
        "--jinja"])
    # the very first request on a fresh card is slow (about 1 tok/s) while the engine sets itself up, so make it here
    import json, time, urllib.request
    key = {"Authorization": f"Bearer {os.environ['ENGINE_KEY']}", "Content-Type": "application/json"}
    for _ in range(600):
        try:
            urllib.request.urlopen("http://127.0.0.1:8080/health", timeout=2); break
        except Exception:
            time.sleep(1)
    for words in ("hi", "Write two sentences about the sea."):
        body = json.dumps({"messages": [{"role": "user", "content": words}], "max_tokens": 32,
                           "chat_template_kwargs": {"enable_thinking": False}}).encode()
        try: urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:8080/v1/chat/completions", body, key), timeout=300).read()
        except Exception as e: print("warm-up:", e)
