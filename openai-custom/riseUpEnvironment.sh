#!/bin/bash
export PATH="$PATH:$HOME/.local/bin"

openai_custom_home=./openai-custom
openai_custom_env=openai-custom-env 

echo "Creating a Python virtual environment..."
python3 -m venv $openai_custom_home/$openai_custom_env

# Step 3: Activate the virtual environment
. $openai_custom_home/$openai_custom_env/bin/activate

pip3 install -r $openai_custom_home/requirements.txt


API_KEY=${API_KEY:=""}


# 
# openai_custom_home=./openai-custom
# echo "$openai_custom_home"

# #pyenv virtualenv 3.8.13 virtualenvironment
# python3 -m virtualenv $openai_custom_home/openai-custom-env 
# . $openai_custom_home/openai-custom-env /bin/activate
# echo "$(python3 -V)"


# pip3 install -r $openai_custom_home/requirements.txt

# API_KEY=${API_KEY:=""}


#python3 ./notebook/main.py  -apiKey "${API_KEY}"}"

# Deactivate the virtual environment
#deactivate

# Remove the virtual environment if desired
#rm -rf notebookEnv

