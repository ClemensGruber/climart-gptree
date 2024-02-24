#!/bin/bash

cd ~/gptree

# activate virtual environment
source venv-gptree/bin/activate

# run GPTree script
python3 main.py

# deactivate virtual environment when script is finished
deactivate