#!/bin/bash

# Setup environment

## Ubuntu Packages
sudo apt update
sudo apt install -y python3-venv python3-pip

## Python environment
python3 -m venv .venv
source ~/.venv/bin/activate
pip install fastapi uvicorn requests

# Run server
sudo .venv/bin/uvicorn main:app --host 0.0.0.0 --port 80