FROM nginx:1.25.3

RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx.conf /etc/nginx/conf.d/
COPY ./ssl-params.conf /etc/nginx/

COPY ./cert_config.conf /etc/nginx/
COPY ./openssl.conf /

COPY ./certs/dhparam.pem /etc/nginx/
COPY ./certs/fullchain.pem /etc/nginx/ssl/
COPY ./privkey.pem /etc/nginx/ssl/

EXPOSE 443

ENTRYPOINT [ "nginx", "-g", "daemon off;" ]