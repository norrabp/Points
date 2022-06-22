#!/bin/bash
process=$1

if [ "$process" == "s" ] || ["$process" == "setup" ]
then
  python3 -m venv env
  source ./env/bin/activate
  pip3 install -r requirements.txt
  PYTHONPATH=. pytest
elif [ "$process" == "r" ] || ["$process" == "run" ]; then
  export FLASK_CONFIG=development
  python3 run.py
elif [ "$process" == "t" ] || ["$process" == "test" ]; then
  export FLASK_CONFIG=testing
  coverage run -m pytest --verbose && coverage report -m
else
  echo "Enter \"s\" or \"setup\" to setup the application,"
  echo "\"r\" or \"run\" to run the flask application,"
  echo "or either \"t\" or \"test\" to run the unit tests."
fi