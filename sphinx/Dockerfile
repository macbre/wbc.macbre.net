# https://hub.docker.com/r/manticoresearch/manticore
FROM manticoresearch/manticore:9.3.2

# set up logs and indices directories
RUN mkdir -pv /opt/sphinx/log /opt/sphinx/index

# redirect logs to stdout
RUN ln -sv /dev/stdout /opt/sphinx/log/query.log
RUN ln -sv /dev/stdout /opt/sphinx/log/searchd.log

# expose TCP port
EXPOSE 36307

VOLUME /opt/sphinx/conf

CMD searchd --nodetach --config /opt/sphinx/conf/sphinx.conf
