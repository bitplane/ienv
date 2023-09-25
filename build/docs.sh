#!/usr/bin/bash

source .venv/bin/activate

set -e

pushd ienv/src
pydoc-markdown -p ienv > ../../docs/pydoc.md
popd

mkdocs build
mkdocs gh-deploy
