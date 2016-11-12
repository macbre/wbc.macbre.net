# wbc.macbre.net

[![Build Status](https://travis-ci.org/macbre/wbc.macbre.net.svg?branch=master)](https://travis-ci.org/macbre/wbc.macbre.net)

[WBC archive](http://www.wbc.poznan.pl/dlibra) served via API and as a web fornt-end application.

## Architecture

[Docker Compose](https://docs.docker.com/compose/install/#/install-docker-compose) running the following:

* SphinxSE instance
* Flask-powered app providing HTTP API

[`macbre/wbc`](https://github.com/macbre/wbc) can fetch and convert DJVU files to XML format that can be indexed by SphinxSE.

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
