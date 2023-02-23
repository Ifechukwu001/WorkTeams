#!/usr/bin/env bash
# Setup to install python modules

sudo apt -y update
sudo apt install -y python3-pip python3-dev python3-setuptools
pip install gunicorn flask sqlalchemy