#!/usr/bin/env bash
set -e

# Notebook to scripts
echo ">> Apply notebook to scripts conversion"
mkdir -p TEMP/
jupyter nbconvert --to script --output-dir TEMP/ notebook/*.ipynb

# Format
echo ">> Apply file formatting"
isort notebook/
black notebook/

# Type checking
echo ">> Apply type checking"
mypy --config-file config/mypy.ini notebook/
mypy --config-file config/mypy.ini TEMP/

# Code quality checking
echo ">> Apply code quality checking"
flake8 --config=config/flake8.ini notebook/
flake8 --config=config/flake8.ini TEMP/

# Done
echo ">> DONE"
