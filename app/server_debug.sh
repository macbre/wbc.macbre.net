export GIT_HASH=`cd .. && git rev-parse HEAD`

REDIS_HOST=0.0.0.0 SPHINX_HOST=127.0.0.1 DEBUG=1 server
