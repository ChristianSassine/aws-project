#!/bin/bash


## Activate Enviornment and make sure the dependencies are updated
echo "Creating python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing python required packages..."
pip install -r requirements.txt

## Launch the process
# This launches the deployment, the benchmark and the cleanup afterwards
echo "Deploying applications..."
python deploy/main.py