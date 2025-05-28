#!/bin/bash

python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
echo "TUI virtual environment and dependencies installed"
