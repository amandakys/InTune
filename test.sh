#!/bin/bash

# Requirements:
# 1. python3
# 2. python3-venv
# 3. Project paths are not modified for:
#    a. requirements.txt (in project root)
#    b. test.sh (this script; in project root)

cd "webapps34"

if [ ! -d "env" ]; then
  python3 -m venv env
fi

# Use virtual env for this block
source env/bin/activate

pip3 install --upgrade pip
pip3 install -r ../requirements.txt

python3 manage.py test

deactivate
# Return back to global python environment

