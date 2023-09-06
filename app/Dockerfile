# Dockerfile for Flask-app
FROM python:3.10-slim

# install venv
RUN pip install virtualenv

RUN mkdir -pv /opt/app
WORKDIR /opt/app
ENV HOME /opt/app
RUN chown nobody .

# use bash so "source" can be used
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

USER nobody
COPY setup.py $HOME/setup.py
RUN pip install -e .

# update the PATH to point to pip's bin/ directory
ENV PATH "$HOME/.local/bin/:$PATH"

# copy the rest of the app to make use of Docker cache layers
COPY . $HOME

# https://docs.docker.com/engine/reference/builder/#healthcheck
#HEALTHCHECK --interval=15s --timeout=1s --retries=3 \
#  CMD wget 0.0.0.0:8080 --spider -q -U 'wget/healthcheck' || exit 1
