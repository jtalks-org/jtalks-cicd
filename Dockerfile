FROM jtalks/base
MAINTAINER Stanislav Bashkyrtsev <stanislav.bashkirtsev@gmail.com>

ENV PYTHONUNBUFFERED 1

USER root
COPY docker-entrypoint.sh /entrypoint
ADD . /home/jtalks/jtalks-cicd
RUN chown -R jtalks ~jtalks && chown jtalks /entrypoint && chmod 700 /entrypoint

USER jtalks
ENTRYPOINT ["/entrypoint"]
