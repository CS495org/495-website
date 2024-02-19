#!/bin/sh
# not used in production, but annoying to deal with it
# every time i want to merge from my dev branch

openssl req -x509 -newkey rsa -keyout /etc/nginx/ssl/key.pem -out /etc/nginx/ssl/cert.pem -days 365 -nodes -config /openssl.conf

nginx -g "daemon off;"