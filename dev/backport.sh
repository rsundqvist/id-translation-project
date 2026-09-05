#!/bin/bash
# Back-port demo edits into the template, then check for un-templatized values.
set -Eeuo pipefail

cd "$(dirname "$0")/.."

python dev/backport.py

echo
echo "--- dev/lint.sh: checking the template for un-templatized values ---"
dev/lint.sh
echo "OK: no concrete values leaked into the template."
