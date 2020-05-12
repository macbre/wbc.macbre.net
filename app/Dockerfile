# Dockerfile for Flask-app
FROM python:3.8-slim

# install venv
RUN pip install virtualenv

RUN mkdir -pv /opt/app
WORKDIR /opt/app
ENV HOME /opt/app

# use bash so "source" can be used
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# setup venv
COPY setup.py $HOME/setup.py

RUN virtualenv -p python3 env
RUN source env/bin/activate
RUN pip install -e .

# copy the rest of the app to make use of Docker cache layers
COPY . $HOME

# https://docs.docker.com/engine/reference/builder/#healthcheck
HEALTHCHECK --interval=15s --timeout=1s --retries=3 \
  CMD wget 0.0.0.0:8080 --spider -q -U 'wget/healthcheck' || exit 1
