# Dockerfile for Sphinx SE
# macbre (c) 2016-2017
FROM debian:stretch
ENV SPHINX_VERSION 3.0.1-7fec4f6

# install dependencies
RUN apt-get update && apt-get install -y wget

# set timezone
# @see http://unix.stackexchange.com/a/76711
RUN cp /usr/share/zoneinfo/CET /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

# set up and expose directories
RUN mkdir -pv /opt/sphinx/log /opt/sphinx/index
VOLUME /opt/sphinx/index

# http://sphinxsearch.com/files/sphinx-3.0.1-7fec4f6-linux-amd64.tar.gz
RUN wget http://sphinxsearch.com/files/sphinx-${SPHINX_VERSION}-linux-amd64.tar.gz -O /tmp/sphinxsearch.tar.gz
RUN cd /opt/sphinx && tar -xf /tmp/sphinxsearch.tar.gz
RUN rm /tmp/sphinxsearch.tar.gz

# point to sphinx binaries
ENV PATH "${PATH}:/opt/sphinx/sphinx-3.0.1-7fec4f6-linux-amd64/bin"
RUN indexer -v

# redirect logs to stdout
RUN ln -sv /dev/stdout /opt/sphinx/log/query.log
RUN ln -sv /dev/stdout /opt/sphinx/log/searchd.log

# home dir
ENV HOME /opt/sphinx
WORKDIR /opt/sphinx
COPY sphinx.conf /opt/sphinx.conf

# expose TCP port
EXPOSE 36307

CMD searchd --nodetach --config /opt/sphinx.conf
