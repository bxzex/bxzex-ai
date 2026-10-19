#!/bin/bash
# Runs every test against a fake model server in a real terminal (a pty), with throwaway folders.
# Nothing touches ~/.bxzex-ai or a real model.   bash tests/run.sh   (about two minutes)
set -u
export BXZEX_NO_TICKER=1   # never touch the real system timer or send notifications
export BXZEX_SKILLS_URL=http://127.0.0.1:9/skills   # never ask bxzex.com from the tests
cd "$(dirname "$0")/.."
APP="$PWD/bxzex-ai"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
ver="$(sed -n 's/^VERSION = "\(.*\)"/\1/p' bxzex-ai)"
fail=0

newer() {   # a copy of the app plus a fake "9.9.9" release for the update tests
  rm -rf "$T/bin" "$T/upd"; mkdir -p "$T/bin" "$T/upd/skills"
  cp bxzex-ai bxzex-server install.sh "$T/bin/"; cp bxzex-server install.sh connectors.txt "$T/upd/";
  sed "s/VERSION = \"$ver\"/VERSION = \"9.9.9\"/" bxzex-ai > "$T/upd/bxzex-ai"; echo "9.9.9 2" > "$T/upd/VERSION"
}

run() {     # name, then the test's arguments
  local name="$1"; shift
  out="$(python3 -I "tests/$name.py" "$@" 2>&1)"
  # "False" is the right answer for these checks: no tracebacks, nothing echoed raw, a blocked file not written, a rewound file gone
  bad="$(echo "$out" | sed -E 's/(tracebacks|echoed|exists|file made): False//g')"
  if echo "$bad" | grep -qE ": False|MISSING|TRACEBACK|tracebacks: True|^Traceback|Error"; then
    echo "FAIL  $name"; echo "$out" | sed 's/^/      /'; fail=1
  else
    echo "ok    $name"
  fi
}
home() { rm -rf "$T/h"; mkdir -p "$T/h"; echo "$T/h"; }

run keys "$APP"
run tools "$APP" "$(home)"
h="$(home)"; printf '# old guide\nstuff\n## Your instructions\nAnything written below this line is from the user. Follow it.\nALWAYS SAY YO\n' > "$h/BXZEX.md"
BXZEX_HOME="$h" run stream_drop "$APP"
run basics "$APP" "$(home)"
run busy_typing "$APP" "$(home)"
run input_box "$APP" "$(home)"
run learner "$APP" "$(home)"
run agent "$APP" "$(home)"
run workflow "$APP" "$(home)"
run phone "$APP" "$(home)"
run footer "$APP" "$(home)"
run ui "$APP" "$(home)" "$PWD/connectors.txt"
newer; run update_reload "$T/bin/bxzex-ai" "$(home)" "$T/upd"
newer; run loaders "$T/bin/bxzex-ai" "$(home)" "$T/upd"

[ $fail = 0 ] && echo "all passed" || { echo "some tests failed"; exit 1; }
