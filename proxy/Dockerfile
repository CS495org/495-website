FROM nginx:1.25.3

RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx.conf /etc/nginx/conf.d/
COPY ./ssl-params.conf /etc/nginx/

# COPY ./cert_config.conf /etc/nginx/
# COPY ./privkey.pem /etc/ssl/private/
# COPY .fullchain.pem /etc/ssl/certs/
# COPY .dhparam.pem /etc/nginx/


EXPOSE 443