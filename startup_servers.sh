#!/usr/bin/env bash
# Start up the web server and api.

cd ~/Workteams && gunicorn --bind 0.0.0.0:80 wsgi:web &
cd ~/Workteams && gunicorn --bind 0.0.0.0:5001 wsgi:api &