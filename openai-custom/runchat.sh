#!/bin/bash
export PATH="$PATH:$HOME/.local/bin"

echo "Creating a Python virtual environment..."
python3 -m venv isoletedEnv 

# Step 3: Activate the virtual environment
. isoletedEnv/bin/activate

pip3 install -r ./openai-custom/requirements.txt


API_KEY=${API_KEY:=""}


python3 ./openai-custom/main.py  -apiKey "${API_KEY}"}"

# Deactivate the virtual environment
deactivate

# Remove the virtual environment if desired
rm -rf isoletedEnv

