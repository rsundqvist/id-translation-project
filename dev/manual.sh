#!/bin/bash

set -e

REPLAY_FILE=dev/manual.json dev/generate-project.sh

cd demo/bci-id-translation && ./setup-and-verify.sh

# poetry run pip install ~/git/id-translation/
# poetry shell
