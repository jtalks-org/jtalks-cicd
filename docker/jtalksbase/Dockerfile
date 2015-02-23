FROM ubuntu:14.04
MAINTAINER Stanislav Bashkyrtsev <stanislav.bashkirtsev@gmail.com>

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

EXPOSE 8080

RUN apt-get -qy install software-properties-common \
 && add-apt-repository ppa:fkrull/deadsnakes \
 # && add-apt-repository  ppa:apt-fast/stable \
 && apt-get update \
 && apt-get -qy install wget unzip python2.6 python-dev libmysqlclient-dev python-mysqldb default-jdk mysql-server \
 && wget -q https://bootstrap.pypa.io/get-pip.py && python get-pip.py \
 # stupid setuptools doesn't seem to have a way to --allow-external inside of itself
 && pip install --allow-external mysql-connector-python mysql-connector-python \
 && echo 'export JAVA_HOME=/usr/lib/jvm/default-java' >> /etc/environment

RUN useradd -d /home/jtalks -M -N -g nogroup -r jtalks  \
 && mkdir ~jtalks \
 && echo 'jtalks ALL = NOPASSWD: ALL' >> /etc/sudoers
RUN chown -R jtalks ~jtalks

USER jtalks
ENV HOME /home/jtalks
WORKDIR /home/jtalks
# installing setuptools
RUN wget -q https://bootstrap.pypa.io/ez_setup.py && python ez_setup.py --user \
 && wget -q http://apache-mirror.rbc.ru/pub/apache/tomcat/tomcat-7/v7.0.59/bin/apache-tomcat-7.0.59.zip \
 && unzip -q apache-tomcat-7.0.59.zip && ln -s apache-tomcat-7.0.59 tomcat \
 && chmod -R 777 tomcat/bin/

