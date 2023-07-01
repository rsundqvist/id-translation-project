#!/bin/bash
set -e
echo "=========================================================================="
echo "|                         VERIFY DEMO PROJECT                            |"
echo "=========================================================================="
echo "-- STEP 1/5: Install with 'poetry' ---------------------------------------"
echo "--------------------------------------------------------------------------"
poetry lock && poetry install

echo "--------------------------------------------------------------------------"
echo "-- STEP 2/5: Format with 'black' and 'isort' -----------------------------"
poetry run black src/ tests/ && isort src/ tests/

echo "--------------------------------------------------------------------------"
echo "-- STEP 3/5: Test with 'pytest' ------------------------------------------"
poetry run pytest

echo "--------------------------------------------------------------------------"
echo "-- STEP 4/5: Lint with 'flake8' ------------------------------------------"
poetry run flake8 src/ tests/ --ignore=E501  # Black enforces line lengths

echo "--------------------------------------------------------------------------"
echo "-- STEP 5/5: Check types with 'mypy' -------------------------------------"
poetry run mypy --non-interactive -p "{{cookiecutter.namespace}}.id_translation" -p "tests.id_translation"

echo "--------------------------------------------------------------------------"
echo "Success! Demo project verified."
