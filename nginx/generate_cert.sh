#!/bin/sh
openssl req -x509 -nodes -days 1825 -newkey rsa:2048 -keyout ssl.key -out ssl.crt
