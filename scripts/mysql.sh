#!/bin/bash

## Exit if an error occurs
set -e

## Setup mysql
sudo apt-get update
sudo apt-get install -y mysql-server
### run mysql_secure_installation (??)
### do we need to assign a user or password? can't we just run with root? (unsecure lmao)

## Sakila

### Download Sakila
wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xzvf sakila-db.tar.gz

### setup sakila in mysql
sudo mysql -u root
SOURCE sakila-db/sakila-schema.sql;
SOURCE sakila-db/sakila-data.sql;
exit

## Benchmark
sudo sysbench /usr/share/sysbench/oltp_read_only.lua --mysql-db=sakila --mysql-user="root" prepare
sudo sysbench /usr/share/sysbench/oltp_read_only.lua --mysql-db=sakila --mysql-user="root" run