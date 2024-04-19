# FROM cgr.dev/chainguard/nginx:latest
FROM nginx:alpine

RUN apk add --update openssl

WORKDIR /

COPY ./nginx.conf /etc/nginx/conf.d/
COPY ./ssl-params.conf /etc/nginx/

COPY ./cert_config.conf /etc/nginx/
COPY ./openssl.conf .
# COPY ./ssl/ /etc/nginx/ssl/
COPY ./startup.sh .

RUN mkdir /etc/nginx/ssl

# COPY .dhparam.pem /etc/nginx/
# not doing DH param on the fly, takes forever, but needs to be included in prod

EXPOSE 443

ENTRYPOINT [ "./startup.sh" ]