#!/bin/sh
export DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4"
docker build --no-cache=true -t jtalks/cicd-tests . || error='Error during image building'
docker run --rm jtalks/cicd-tests || error='Error during container run'
docker rmi jtalks/cicd-tests
if [ ! -z "$error" ]; then
  echo "$error"
  docker rmi $(docker images | grep '^<none>' | awk '{print $3}')
  exit 1
fi
