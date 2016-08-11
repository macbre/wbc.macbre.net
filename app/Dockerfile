# Dockerfile for Flask-app
FROM python:3.4-alpine

# Fix Searching for pytest==2.8.2
# Reading https://pypi.python.org/simple/pytest/
# Download error on https://pypi.python.org/simple/pytest/: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:600) -- Some packages may not be found!
# Couldn't find index page for 'pytest' (maybe misspelled?)
RUN apk --update upgrade && \
    apk add curl ca-certificates && \
    update-ca-certificates && \
    rm -rf /var/cache/apk/*

# install venv
RUN pip install virtualenv

RUN mkdir -pv /opt/app
WORKDIR /opt/app
ENV HOME /opt/app

ADD . /opt/app

# setup venv
RUN virtualenv -p python3 env
RUN source env/bin/activate
RUN pip install -e .
