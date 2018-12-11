#!/bin/bash

[ -d venv ] || ./setup.sh
. ./venv/bin/activate

python3 dev.py
