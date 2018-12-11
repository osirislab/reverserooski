#!/bin/bash

[ -d venv ] && echo "rm -rf venv" && rm -rf venv

pip3 install virtualenv
virtualenv -p $(which python3) venv
. ./venv/bin/activate

pip3 install -r requirements.txt
