FROM ubuntu:14.04
MAINTAINER Stanislav Bashkyrtsev <stanislav.bashkirtsev@gmail.com>

ENV PYTHONUNBUFFERED 1

RUN apt-get -qy install software-properties-common \
 && add-apt-repository ppa:fkrull/deadsnakes \
 && apt-get update \
 && apt-get -qy install wget python2.7 python-dev libmysqlclient-dev python-mysqldb

RUN useradd -d /home/jtalks -M -N -g nogroup -r jtalks && mkdir ~jtalks
ADD . /home/jtalks/jtalks-cicd
RUN chown -R jtalks ~jtalks
RUN wget -q https://bootstrap.pypa.io/get-pip.py && python get-pip.py \
# stupid setuptools doesn't seem to have a way to --allow-external inside of itself
 && pip install --allow-external mysql-connector-python mysql-connector-python

USER jtalks
ENV HOME /home/jtalks
WORKDIR /home/jtalks/jtalks-cicd
RUN wget -q https://bootstrap.pypa.io/ez_setup.py && python ez_setup.py --user && ./setup.py install

RUN cp -r tests/.jtalks ~/
CMD ["./setup.py", "test"]