#!/usr/bin/env bash
# Start up the web server and api.

sudo apt install authbind
sudo touch /etc/authbind/byport/80
sudo chmod 500 /etc/authbind/byport/80
sudo chown $USER /etc/authbind/byport/80
sudo apt-get build-dep python-mysqldb
pip install mysqlclient
sudo apt-get install python3-pip python3-dev libmysqlclient-dev


cd ~/WorkTeams 
export WT_STORAGE=db WT_USER=wt_user WT_HOST=localhost WT_PASS=wt_pass WT_DB=wt_db
mkdir -p ~/WorkTeams/log/gunicorn
touch ~/WorkTeams/log/gunicorn/access_log_wtweb
touch ~/WorkTeams/log/gunicorn/access_log_wtapi
touch ~/WorkTeams/log/gunicorn/error_log_wtweb
touch ~/WorkTeams/log/gunicorn/error_log_wtapi
chmod go+w ~/WorkTeams/log/gunicorn/*

authbind gunicorn -c gunicorn_webconf.py wsgi:web &
gunicorn -c gunicorn_apiconf.py  wsgi:api &
exit
