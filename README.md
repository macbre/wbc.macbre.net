# wbc.macbre.net

[![Build Status](https://travis-ci.org/macbre/wbc.macbre.net.svg?branch=master)](https://travis-ci.org/macbre/wbc.macbre.net)

[WBC archive](http://www.wbc.poznan.pl/dlibra) served via API and as a web fornt-end application.

## Architecture

[Docker Compose](https://docs.docker.com/compose/install/#/install-docker-compose) running the following:

* SphinxSE instance
* Flask-powered app providing HTTP API

[`macbre/wbc`](https://github.com/macbre/wbc) can fetch and convert DJVU files to XML format that can be indexed by SphinxSE.

## Development

Run the following:

```
docker-compose up -d sphinx
cd app && virtualenv env && source env/bin/activate && pip install -e . && ./server_debug.sh
```

The local instance of wbc.macbre.net should be ready at `http://0.0.0.0:8080/`

## API

> Needs to be prefixed with `/api/v1` (e.g. `/api/v1/search?q=foo`)

### Publications

##### `GET /publications`

List of all publications

##### `GET /publications/{id}`

Meta data of a given publication

### Issues

##### `GET /issues/{id}`

Get all documents in a given issue

### Documents

##### `GET /documents/{id}`

Get a given document

##### `GET /documents/{id}.txt`

Get a given document in txt file format

### Search

##### `GET /search?q={query}`

Search within all publications

### Suggest

##### `GET /suggest?q={query}`

Return [search suggestions](http://www.opensearch.org/Specifications/OpenSearch/Extensions/Suggestions/1.1)

## schema.org

* https://schema.org/PublicationIssue
* https://schema.org/PublicationVolume

## Certificate renewal

```sh
acme.sh --issue -d wbc.macbre.net  --stateless --force
```

## Content indexing

* get XML content from http://s3.macbre.net/wbc/106644.xml.gz (indexed by [`macbre/wbc`](https://github.com/macbre/wbc))
* run `make index` to index XML file in sphinx

```
using config file '/opt/sphinx.conf'...
indexing index 'wbc'...
collected 6968 docs, 123.9 MB
sorted 17.0 Mhits, 100.0% done
total 6968 docs, 123948611 bytes
total 22.636 sec, 5475608 bytes/sec, 307.82 docs/sec
total 510 reads, 2.005 sec, 423.4 kb/call avg, 3.9 msec/call avg
total 1418 writes, 0.324 sec, 303.6 kb/call avg, 0.2 msec/call avg
```
