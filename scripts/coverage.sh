#!/bin/sh

. ./scripts/activate.sh

pytest --cov="src/$1" --cov-report=html .
