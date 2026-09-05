#!/bin/bash
set -Eeuo pipefail

exec python "$(dirname "$0")/lint.py" "$@"
