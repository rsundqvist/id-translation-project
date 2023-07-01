#!/bin/bash

set -e

REPLAY_FILE=dev/manual.json dev/generate-project.sh

cd demo/bci-id-translation && ./verify-demo-project.sh

# poetry run pip install ~/git/id-translation/
# poetry shell
