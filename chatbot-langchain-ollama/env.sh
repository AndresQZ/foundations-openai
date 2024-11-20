#!/bin/bash
export PATH="$PATH:$HOME/.local/bin"

echo "Creating a Python virtual environment..."
python3 -m venv chatbotLangchainEnv

# Step 3: Activate the virtual environment
. chatbotLangchainEnv/bin/activate

pip3 install -r ./chatbot-langchain-ollama/requirements.txt


API_KEY=${API_KEY:=""}


#python3 ./notebook/main.py  -apiKey "${API_KEY}"}"

# Deactivate the virtual environment
#deactivate

# Remove the virtual environment if desired
#rm -rf chatbotLangchainEnv

