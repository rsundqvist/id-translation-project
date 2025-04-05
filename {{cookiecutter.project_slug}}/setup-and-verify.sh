#!/bin/bash
set -eu

cd "$(dirname "$0")"

echo "=========================================================================="
echo "|                         VERIFY DEMO PROJECT                            |"
echo "=========================================================================="
echo "-- STEP 1/6: Install with 'poetry' ---------------------------------------"
echo "--------------------------------------------------------------------------"
poetry lock
poetry install
eval "$(poetry env activate)"

echo "--------------------------------------------------------------------------"
echo "-- STEP 2/6: Format with 'ruff' ------------------------------------------"
ruff format src/ tests/

echo "--------------------------------------------------------------------------"
echo "-- STEP 3/6: Test with 'pytest' ------------------------------------------"
pytest tests/

echo "--------------------------------------------------------------------------"
echo "-- STEP 4/6: Lint with 'ruff' --------------------------------------------"
ruff check src/ tests/

echo "--------------------------------------------------------------------------"
echo "-- STEP 5/6: Check types with 'mypy' -------------------------------------"
mypy --non-interactive -p "{{cookiecutter.namespace}}.id_translation" -p "tests.id_translation"

echo "--------------------------------------------------------------------------"
echo "-- STEP 6/6: Generate documentation with 'sphinx' ------------------------"
sphinx-build docs/ docs/_build

echo "-------------------------------- Success! --------------------------------"
echo "Demo project verified. To see the generated documentation, run:"
echo "    open docs/_build/index.html"
