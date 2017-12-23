# Dockerfile for ngnix
FROM nginx:1.13.7-alpine
RUN rm /etc/nginx/conf.d/default.conf

# basic configs
COPY gzip.conf /etc/nginx/conf.d/

# copy the site config file
COPY site.conf /etc/nginx/conf.d/

# caching
COPY caching.conf /etc/nginx/conf.d/

# SSL certificate
# ssl.key and ssl.crt files
# https://github.com/macbre/wbc.macbre.net/issues/21
RUN mkdir /etc/nginx/cert/
COPY wbc.macbre.net.* /etc/nginx/cert/

# redirect errors and access log
RUN rm -f /var/log/nginx/*
RUN ln -s /dev/stderr /var/log/nginx/error.log
RUN ln -s /dev/stdout /var/log/nginx/access.log
