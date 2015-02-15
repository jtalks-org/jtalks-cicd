#!/bin/sh
docker build -t jtalks/cicd-tests . || error='Error during image building'
docker run --rm jtalks/cicd-tests || error='Error during container run'
docker rmi jtalks/cicd-tests
if [ ! -z "$error" ]; then
  docker rmi $(docker images | grep '^<none>' | awk '{print $3}')
  echo "$error"
  exit 1
fi