#!/bin/sh
set -xe

start=$(date +%s.%N)

$(docker images | grep 'jtalks/base') || \
  docker build --no-cache=true -t jtalks/base docker/jtalksbase || error='Error during base image building'

docker build --no-cache=true -t jtalks/cicd-tests . || error='Error during image building'
docker run --rm jtalks/cicd-tests || error='Error during container run'
docker rmi jtalks/cicd-tests || echo 'No previously created image, creating one.'
if [[ "$1_" == '-cleanup_' ]]; then
  docker rmi jtalks/base
fi
if [ ! -z "$error" ]; then
  echo "$error"
  docker rmi $(docker images | grep '^<none>' | awk '{print $3}')
  exit 1
fi

end=$(date +%s.%N)
