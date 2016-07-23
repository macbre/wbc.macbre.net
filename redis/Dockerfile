# Dockerfile for redis
FROM debian:sid

# use bash to have 'source' command
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# install dependencies
RUN apt-get update && apt-get install -y redis-server

# set timezone
# @see http://unix.stackexchange.com/a/76711
RUN cp /usr/share/zoneinfo/CET /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

# set up directories
RUN mkdir -pv /opt/redis/

ENTRYPOINT ["redis-server", "--appendonly", "yes", "--appendfsync", "everysec", "--bind", "0.0.0.0", "--dir", "/opt/redis", "--loglevel", "notice"]
