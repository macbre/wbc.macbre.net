# Dockerfile for ngnix
FROM nginx:1.11.1-alpine
RUN rm /etc/nginx/conf.d/default.conf

# basic configs
COPY gzip.conf /etc/nginx/conf.d/

# copy the site config file
COPY site.conf /etc/nginx/conf.d/

# caching
COPY caching.conf /etc/nginx/conf.d/

# SSL certificate
RUN mkdir /etc/nginx/cert/
COPY ssl.* /etc/nginx/cert/

# redirect errors and access log
RUN rm -f /var/log/nginx/*
RUN ln -s /dev/stderr /var/log/nginx/error.log
RUN ln -s /dev/stdout /var/log/nginx/access.log
