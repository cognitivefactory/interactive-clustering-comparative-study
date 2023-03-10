#!/usr/bin/env bash
set -e

# Notebook to scripts
echo ">> Apply notebook to scripts conversion"
mkdir -p .temp/
jupyter nbconvert --to script --output-dir .temp/ */notebook/*.ipynb

# Format
echo ">> Apply file formatting"
isort */notebook/
black */notebook/

# Type checking
echo ">> Apply type checking"
mypy --config-file config/mypy.ini */notebook/
mypy --config-file config/mypy.ini .temp/

# Code quality checking
echo ">> Apply code quality checking"
flake8 --config=config/flake8.ini */notebook/
flake8 --config=config/flake8.ini .temp/

# Done
echo ">> DONE"
