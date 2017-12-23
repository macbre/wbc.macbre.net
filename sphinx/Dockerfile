# Dockerfile for Sphinx SE
# macbre (c) 2016-2017
FROM debian:jessie

# install dependencies
RUN apt-get update && apt-get install -y wget

ENV SPHINX_VERSION 2.3.2-beta

RUN wget http://sphinxsearch.com/files/sphinxsearch_${SPHINX_VERSION}-1~jessie_amd64.deb -O /tmp/sphinxsearch.deb
RUN dpkg -i /tmp/sphinxsearch.deb || apt-get -f install -y

# set timezone
# @see http://unix.stackexchange.com/a/76711
RUN cp /usr/share/zoneinfo/CET /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

# set up directories
RUN mkdir -pv /opt/sphinx/log /opt/sphinx/index/wbc

# redirect logs to stdout
RUN ln -sv /dev/stdout /opt/sphinx/log/query.log
RUN ln -sv /dev/stdout /opt/sphinx/log/searchd.log

# home dir
ENV HOME /opt/sphinx
WORKDIR /opt/sphinx
COPY sphinx.conf /opt/sphinx.conf

# expose TCP port
EXPOSE 36307
