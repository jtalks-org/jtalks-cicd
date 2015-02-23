#!/bin/sh
start=$(date +%s.%N)

jtalks_base=`docker images | grep 'jtalks/base'`
if [ -z "$jtalks_base" ]; then
  docker build --no-cache=true -t jtalks/base docker/jtalksbase || error='Error during base image building'
fi
docker build --no-cache=true -t jtalks/cicd-tests . || error='Error during image building'
docker run --rm jtalks/cicd-tests || error='Error during container run'
docker rmi jtalks/cicd-tests
if [ "$1" == '-cleanup' ]; then
  docker rmi jtalks/base
fi
if [ ! -z "$error" ]; then
  echo "$error"
  docker rmi $(docker images | grep '^<none>' | awk '{print $3}')
  exit 1
fi

end=$(date +%s.%N)
diff=$(echo "$end - $start" | bc)
echo "Script took $diff sec"
