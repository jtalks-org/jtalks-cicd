#!/bin/sh
docker build -t jtalks/cicd-tests .
docker run --rm jtalks/cicd-tests
docker rmi jtalks/cicd-tests || docker rmi $(docker images | grep '^<none>' | awk '{print $3}')