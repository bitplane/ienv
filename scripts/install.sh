#!/bin/sh

. ./scripts/activate.sh

set -e

# install our package
python3 -m pip install .

# let make know that we are installed in user mode
echo Installed normally

touch .venv/.installed
rm .venv/.installed-dev || true

