#!/bin/sh

# no longer used

openssl req -x509 -newkey rsa -keyout /etc/nginx/ssl/key.pem -out /etc/nginx/ssl/cert.pem -days 365 -nodes -config /openssl.conf
# openssl req -x509 -newkey rsa -keyout ./proxy/ssl/key.pem -out ./proxy/ssl/cert.pem -days 365 -nodes -config /openssl.conf

nginx -g "daemon off;"