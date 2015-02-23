FROM jtalks/base
MAINTAINER Stanislav Bashkyrtsev <stanislav.bashkirtsev@gmail.com>

ENV PYTHONUNBUFFERED 1

USER root
ADD configs_example /home/jtalks/.jtalks
RUN chown -R jtalks ~jtalks && pip install jtalks-cicd

USER jtalks
