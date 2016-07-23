# wbc.macbre.net

[WBC archive](http://www.wbc.poznan.pl/dlibra) served via API and as a SLA application.

## Architecture

Docker running the following:

* SphinxSE instance
* Redis as a caching layer
* Flask-powered app providing HTTP API

[`macbre/wbc`](https://github.com/macbre/wbc) can fetch and convert DJVU files to XML format that can be indexed by SphinxSE.

## API

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

##### `GET /publications?q={query}`

Search within all publications


## schema.org

* https://schema.org/PublicationIssue
* https://schema.org/PublicationVolume
