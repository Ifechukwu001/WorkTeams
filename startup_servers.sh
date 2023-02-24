#!/usr/bin/env bash
# Start up the web server and api.

sudo apt install authbind
sudo touch /etc/authbind/byport/80
sudo chmod 500 /etc/authbind/byport/80
sudo chown $USER /etc/authbind/byport/80
cd ~/WorkTeams && authbind gunicorn --bind 0.0.0.0:80 wsgi:web &
cd ~/WorkTeams && gunicorn --bind 0.0.0.0:5001 wsgi:api &