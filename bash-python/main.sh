#!/bin/bash

echo "VAR": $VAR

export PATH="$PATH:$HOME/.local/bin"

echo "python virtual environment"
python3 -m venv virtualEnvironment

# active it
. virtualEnvironment/bin/activate

pip3 install -r ./bash-python/requirements.txt

#writting default env variables

VAR=${VAR:=""}

# run main python file

python3 ./bash-python/bash-python/main.py -mode "${VAR}"

#deactivate virtual
deactivate

#get rid of virtual

rm -rf virtualEnvironment