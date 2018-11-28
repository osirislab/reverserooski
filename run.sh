#!/bin/bash

[ -d venv ] || ./setup.sh
. ./venv/bin/activate
python main.py
