#!/bin/sh
docker build -t jtalks/cicd-tests .
docker run jtalks/cicd-tests --rm