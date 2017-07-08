nginx
=====

## Setting up acme.sh

```
curl https://get.acme.sh | sh
acme.sh --register-account

[Sat Jul  8 20:52:24 CEST 2017] ACCOUNT_THUMBPRINT='xxxx'
```

Put `ACCOUNT_THUMBPRINT` in `site.conf` file.

## Renewing certificates

```
acme.sh --stateless --issue -d wbc.macbre.net
```
