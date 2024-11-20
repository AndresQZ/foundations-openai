#!/bin/bash
export PATH="$PATH:$HOME/.local/bin"

echo "Creating a Python virtual environment..."
python3 -m venv notebookEnv 

# Step 3: Activate the virtual environment
. notebookEnv/bin/activate

pip3 install -r ./notebook/requirements.txt


API_KEY=${API_KEY:=""}


#python3 ./notebook/main.py  -apiKey "${API_KEY}"}"

# Deactivate the virtual environment
#deactivate

# Remove the virtual environment if desired
#rm -rf notebookEnv

