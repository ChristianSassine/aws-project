#!/bin/bash

MYSQL_USERNAME="projectUser"
MYSQL_USER_PASSWORD="ukMULbEQ@;U8B"

## Exit if an error occurs
set -e

# Download packages
sudo apt-get update
sudo apt-get install -y mysql-server sysbench python3-venv python3-pip

## Setup mysql
### Secure mysql with mysql_secure_installation script
sudo mysql_secure_installation --use-default
### Add new user
sudo mysql -e "CREATE USER '$MYSQL_USERNAME'@'localhost' IDENTIFIED BY '$MYSQL_USER_PASSWORD';"
sudo mysql -e "GRANT ALL PRIVILEGES ON *.* TO '$MYSQL_USERNAME'@'localhost' WITH GRANT OPTION;"
sudo mysql -e "FLUSH PRIVILEGES;"

## Sakila

### Download Sakila
wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xzvf sakila-db.tar.gz

### setup sakila in mysql
sudo mysql -e "SOURCE sakila-db/sakila-schema.sql;"
sudo mysql -e "SOURCE sakila-db/sakila-data.sql;"

## Benchmark
sudo sysbench /usr/share/sysbench/oltp_read_only.lua --mysql-db=sakila --mysql-user="$MYSQL_USERNAME" --mysql-password="$MYSQL_USER_PASSWORD" prepare
sudo sysbench /usr/share/sysbench/oltp_read_only.lua --mysql-db=sakila --mysql-user="$MYSQL_USERNAME" --mysql-password="$MYSQL_USER_PASSWORD" run

# ## Python environment
# python3 -m venv .venv
# source ~/.venv/bin/activate
# pip install fastapi uvicorn requests

# # Run server
# sudo .venv/bin/uvicorn main:app --host 0.0.0.0 --port 80