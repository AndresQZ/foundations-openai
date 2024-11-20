#!/bin/bash
PYENV_HOME=./ragWithMongoDb/ragMongoDbEnv
echo "$PYENV_HOME"

#pyenv virtualenv 3.8.13 virtualenvironment
python3 -m virtualenv ./ragWithMongoDb/ragMongoDbEnv 
. $PYENV_HOME/bin/activate
echo "$(python3 -V)"


pip3 install -r ./ragWithMongoDb/requirements.txt