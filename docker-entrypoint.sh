#!/bin/sh
sudo service mysql start
cd ~/jtalks-cicd
python setup.py test
