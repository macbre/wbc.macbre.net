export GIT_HASH=`cd .. && git rev-parse HEAD`

REDIS_HOST=0.0.0.0 SPHINX_HOST=0.0.0.0 DEBUG=1 server
