#!/usr/bin/env bash

source .venv/bin/activate

pytest --cov=ienv/src --cov-report=html .
