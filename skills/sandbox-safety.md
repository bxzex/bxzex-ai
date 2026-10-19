---
name: sandbox-safety
description: Running untrusted or generated code safely with containers, no network, resource limits and throwaway directories.
---
# Running Untrusted or Generated Code Safely

Treat any code you did not write, and any code you just generated, as hostile until proven otherwise.

1. **Read it first.** Skim for `rm -rf`, `curl | sh`, network calls, reads of `~/.ssh`, `.env`, browser data, and writes outside the project. If you cannot explain a line, do not run it.
2. **Use a throwaway directory.** `d=$(mktemp -d) && cd "$d"`. Copy in only the files it needs. Delete the folder afterward.
3. **Use a container with no network.**
   ```
   docker run --rm -it \
     --network none \
     --memory 512m --cpus 1 --pids-limit 128 \
     --read-only --tmpfs /tmp \
     --cap-drop ALL --security-opt no-new-privileges \
     --user 1000:1000 \
     -v "$d":/work:ro -w /work python:3.12-slim python script.py
   ```
   Mount the code read-only. If it must write output, mount a separate empty folder for that. If it needs packages, install them in a first step with network on, then run the code with network off.
4. **Never run as root, never use `sudo`**, and never use `--privileged` or mount `/var/run/docker.sock`, your home folder or the real project with write access.
5. **No real data or secrets.** Use fake sample files and an empty environment: `env -i` or a clean container. Do not pass API keys.
6. **Limit time.** Wrap runs: `timeout 30 <command>`. Kill runaway output with `| head -c 100000`.
7. **Without Docker** (last resort): run as a separate low-privilege user, use `ulimit -t 30 -v 1000000`, and on Linux `unshare -n` for no network. Tell the user this is weaker than a container.
8. **Inspect results as data.** Read output files as text; do not execute them or open them in an app that runs macros.

**Check:** inside the container, `curl -m 3 https://example.com` should fail and `touch /work/x` should fail on a read-only mount.

**Pitfalls:** assuming a virtualenv is a sandbox (it is not); leaving a container running after the test; forgetting that installing a package can itself run code.
