FROM nginx:1.25.3-alpine3.18-slim

RUN rm /etc/nginx/conf.d/default.conf

# COPY ./static/ /static

COPY ./nginx.conf /etc/nginx/conf.d/
COPY ./ssl-params.conf /etc/nginx/

COPY ./cert_config.conf /etc/nginx/

RUN mkdir -p /etc/nginx/ssl

COPY ./certs/* /etc/nginx/ssl/

EXPOSE 443

ENTRYPOINT [ "nginx", "-g", "daemon off;" ]