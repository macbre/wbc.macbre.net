# Dockerfile for Flask-app
FROM debian:jessie

# use bash to have 'source' command
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# install dependencies
RUN apt-get update && apt-get install -y \
	python3-minimal python3-pip virtualenv

# set timezone
# @see http://unix.stackexchange.com/a/76711
RUN cp /usr/share/zoneinfo/CET /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

RUN mkdir /opt/app
WORKDIR /opt/app
ENV HOME /opt/app

ADD . /opt/app

RUN virtualenv -p python3 env
RUN source env/bin/activate
RUN python3 setup.py install
