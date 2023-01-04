#!/usr/bin/env bash
# Script to setup the database.

sudo apt update -y
sudo apt install -y mysql-server
sudo service mysql start

sudo mysql << _EOF_
CREATE DATABASE IF NOT EXISTS wt_db;
CREATE USER IF NOT EXISTS 'wt_user'@'localhost' IDENTIFIED BY 'wt_pass';
GRANT ALL PRIVILEGES ON wt_db.* TO 'wt_user'@'localhost';
FLUSH PRIVILEGES;
_EOF_

if [ -z "$WT_USER" ]
	sed -i "\$a\export WT_STORAGE=db WT_USER=wt_user WT_HOST=localhost WT_PASS=wt_pass WT_DB=wt_db" /etc/profile
	echo "Restarting your machine... Save all work progress and press ENTER when ready."
	read
	sudo reboot
fi
