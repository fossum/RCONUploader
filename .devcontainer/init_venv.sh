#!/bin/bash
# Must be run from the root of the project.

mkdir -p .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
