nginx
=====

SSL certificates are handled by Traefik, nginx gets plain HTTP requests.

### Cache

To use cache set the `cache/` directory ownership:

```
sudo chown 100:101 cache/
```

```
$ curl 'https://wbc.macbre.net/static/wbc.48212b50.min.css' --compressed -i  2>&1 | grep -iE 'cache|encoding'
cache-control: public, max-age=31536000
content-encoding: zstd
x-cache: HIT
```
