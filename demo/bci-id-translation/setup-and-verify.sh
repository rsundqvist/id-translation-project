#!/bin/bash
set -e

echo "=========================================================================="
echo "|                         VERIFY DEMO PROJECT                            |"
echo "=========================================================================="
echo "-- STEP 1/6: Install with 'poetry' ---------------------------------------"
echo "--------------------------------------------------------------------------"
poetry lock && poetry install
source "$(poetry env info --path)/bin/activate"

echo "--------------------------------------------------------------------------"
echo "-- STEP 2/6: Format with 'black' and 'isort' -----------------------------"
black src/ tests/ && isort src/ tests/

echo "--------------------------------------------------------------------------"
echo "-- STEP 3/6: Test with 'pytest' ------------------------------------------"
pytest tests/

echo "--------------------------------------------------------------------------"
echo "-- STEP 4/6: Lint with 'flake8' ------------------------------------------"
flake8 src/ tests/ --ignore=E501  # Black enforces line lengths

echo "--------------------------------------------------------------------------"
echo "-- STEP 5/6: Check types with 'mypy' -------------------------------------"
mypy --non-interactive -p "big_corporation_inc.id_translation" -p "tests.id_translation"

echo "--------------------------------------------------------------------------"
echo "-- STEP 6/6: Generate documentation with 'sphinx' ------------------------"
sphinx-build docs/ docs/_build

echo "-------------------------------- Success! --------------------------------"
echo "Demo project verified. To see the generated documentation, run:"
echo "    open docs/_build/index.html"
