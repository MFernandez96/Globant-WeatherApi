# Globant-WeatherApi

Django API for work interview.

# Remember to install pip

sudo apt-get update
sudo apt-get upgrade #Optional
sudo apt install python3-pip
export PATH=/home/<user_name>/.local/bin:$PATH

# Install into your env

pip install -r requirements/base.txt

# Load env variables

export PYTHONPATH={PATH_TO_REPO}:$PYTHONPATH
set -o allexport; source environments/local; set +o allexport
export DJANGO_ALLOW_ASYNC_UNSAFE=True

# How to run

python3 manage.py runserver

# run tests

pytest

# see coverage

coverage run -m pytest
coverage report
