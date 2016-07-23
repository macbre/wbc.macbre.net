# Dockerfile for Sphinx SE
# macbre (c) 2016
FROM debian:sid

# use bash to have 'source' command
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# install dependencies
RUN apt-get update && apt-get install -y wget

RUN wget http://sphinxsearch.com/files/sphinxsearch_2.2.10-release-1~jessie_amd64.deb -O /tmp/sphinxsearch.deb
RUN dpkg -i /tmp/sphinxsearch.deb || apt-get -f install -y

# set timezone
# @see http://unix.stackexchange.com/a/76711
RUN cp /usr/share/zoneinfo/CET /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

# set up directories
RUN mkdir -pv /opt/sphinx/log /opt/sphinx/index/wbc

# redirect logs to stdout
RUN ln -sv /dev/stdout /opt/sphinx/log/query.log

# home dir
ENV HOME /opt/sphinx
WORKDIR /opt/sphinx
COPY sphinx.conf /opt/sphinx.conf
