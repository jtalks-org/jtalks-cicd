#!/bin/sh
sudo service mysql start
cd ~/jtalks-cicd
./setup.py install && cp -r tests/.jtalks ~/
python setup.py test
