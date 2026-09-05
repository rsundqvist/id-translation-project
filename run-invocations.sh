#!/bin/bash
set -e

echo "---------- run-invocations.sh -----------"
echo "1/4: Clean -------------------------------"
uv run inv clean
echo "2/4: Format code -------------------------"
uv run inv format
echo "3/4: Lint ---------------------------------"
uv run inv lint
echo "4/4: Test ---------------------------------"
uv run inv tests
echo "---------------- Finished ---------------"
