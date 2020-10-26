#!/bin/bash

#install the latest Python 3 version
sudo apt-get update
sudo apt-get install python3.8

#install pip
sudo apt-get install -y python3-pip
sudo apt-get install build-essential libssl-dev libffi-dev python-dev

# install redis
sudo apt update -y
sudo apt install redis-server -y
systemctl daemon-reload
sudo systemctl restart redis.service

#install virtual environment
sudo apt-get install -y python3-venv

#create virtual environment
python3 -m venv venv

#activate virtual environment
source venv/bin/activate
pip install -r requirements.txt

# migrate
python manage.py migrate