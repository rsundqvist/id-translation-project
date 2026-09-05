#!/bin/bash
set -eu

cd "$(dirname "$0")"

echo "=========================================================================="
echo "|                   VERIFY bci-id-translation"
echo "=========================================================================="
echo "-- STEP 1/6: Install with 'uv' -------------------------------------------"
echo "--------------------------------------------------------------------------"
uv lock
uv sync
source .venv/bin/activate

echo "--------------------------------------------------------------------------"
echo "-- STEP 2/6: Format with 'ruff' ------------------------------------------"
ruff format --check src/ tests/  # Verify; without --check this rewrites the code and always exits 0.

echo "--------------------------------------------------------------------------"
echo "-- STEP 3/6: Test with 'pytest' ------------------------------------------"
pytest tests/

echo "--------------------------------------------------------------------------"
echo "-- STEP 4/6: Lint with 'ruff' --------------------------------------------"
ruff check --no-fix src/ tests/  # Without --no-fix, 'fix = true' rewrites the code and exits 0.

echo "--------------------------------------------------------------------------"
echo "-- STEP 5/6: Check types with 'mypy' -------------------------------------"
mypy -p "big_corporation_inc.id_translation" -p "tests.id_translation"

echo "--------------------------------------------------------------------------"
echo "-- STEP 6/6: Generate documentation with 'sphinx' ------------------------"
sphinx-build -W --keep-going docs/ docs/_build

echo "-------------------------------- Success! --------------------------------"
echo "Verified. To see the generated documentation, run:"
echo "    open docs/_build/index.html"
