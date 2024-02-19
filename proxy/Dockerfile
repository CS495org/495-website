FROM nginx:1.25.3-alpine3.18-slim

RUN apk add --update openssl

RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx.conf /etc/nginx/conf.d/
COPY ./ssl-params.conf /etc/nginx/

COPY ./cert_config.conf /etc/nginx/
COPY ./openssl.conf /
# COPY .dhparam.pem /etc/nginx/
# not doing DH param on the fly, takes forever, but needs to be included in prod

EXPOSE 443

COPY ./startup.sh /
# RUN chmod ugo+rwx /startup.sh

RUN mkdir /etc/nginx/ssl
# idk why openssl doesn't want to make the dir, maybe there's a -p flag or something
# not important for now

ENTRYPOINT [ "/startup.sh" ]