#!/bin/bash

apt-get -y update
apt-get -y upgrade
apt-get -y install python-pip
pip install flask
apt-get install postgresql-9.3
# apt-get install postgresql-client
# TODO: setup psql server
