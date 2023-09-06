# Dockerfile for Flask-app
FROM python:3.10-slim

# set up the working directory
WORKDIR /opt/app
ENV HOME /opt/app
COPY setup.py setup.py
RUN chown -Rv nobody:nogroup .

# update the PATH to point to pip's bin/ directory
ENV PATH "$HOME/.local/bin/:$PATH"

RUN pip install --no-cache --user -e .

# copy the rest of the app to make use of Docker cache layers
COPY . $HOME

# permission fixes
RUN chown -Rv nobody ./wbc/static/

# make the container run using the nobody user
USER nobody

# sanity checks
RUN python --version; gunicorn -v

# https://docs.docker.com/engine/reference/builder/#healthcheck
#HEALTHCHECK --interval=15s --timeout=1s --retries=3 \
#  CMD wget 0.0.0.0:8080 --spider -q -U 'wget/healthcheck' || exit 1
