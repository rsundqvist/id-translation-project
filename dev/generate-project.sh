#!/bin/bash
set -Eeuo pipefail

cd "$(dirname "$0")/.."

REPLAY_FILE="${REPLAY_FILE:-tests/replay/master.json}"
OUTPUT_DIR=demo
PROJECT_DIR="$OUTPUT_DIR/bci-id-translation"

rm -rf "$PROJECT_DIR"
cookiecutter . --replay-file "$REPLAY_FILE" -f --output-dir $OUTPUT_DIR

# Cookiecutter exits 0 even when rendering fails, leaving a half-written project behind
# (see tests/test_bake_project.py). Without this, 'inv generate-demo' reports success and
# the damage only surfaces later, in whatever ran next.
for required in pyproject.toml setup-and-verify.sh src tests docs; do
  if [ ! -e "$PROJECT_DIR/$required" ]; then
    echo "FAIL: cookiecutter exited 0 but '$PROJECT_DIR/$required' is missing." >&2
    exit 1
  fi
done

# Regenerating from demo/replay.json itself is the documented way to refresh the committed
# demo, and 'cp' fails on a same-file copy -- which 'set -e' would turn into a failed run.
if [ "$REPLAY_FILE" -ef "$OUTPUT_DIR/replay.json" ]; then
  echo "Replay file is already $OUTPUT_DIR/replay.json; nothing to copy."
else
  cp "$REPLAY_FILE" $OUTPUT_DIR/replay.json
fi
