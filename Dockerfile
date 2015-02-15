FROM ubuntu:14.04
MAINTAINER Stanislav Bashkyrtsev <stanislav.bashkirtsev@gmail.com>

RUN apt-get -qy install software-properties-common \
 && add-apt-repository ppa:fkrull/deadsnakes \
 && apt-get update \
 && apt-get -qy install wget python2.7 python-dev libmysqlclient-dev python-mysqldb

RUN useradd -d /home/jtalks -M -N -g nogroup -r jtalks && mkdir ~jtalks
ADD . /home/jtalks/jtalks-cicd
RUN chown -R jtalks ~jtalks
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py

USER jtalks
WORKDIR /home/jtalks/jtalks-cicd
RUN mkdir ~/.pip-packages
ENV PYTHONPATH=$PYTHONPATH:/home/jtalks/.pip-packages:.:tests
RUN ./setup.py --help install && ./setup.py install --user --install-lib=~/.pip-packages && cp -r tests/.jtalks ~/
CMD ["./setup.py", "test"]