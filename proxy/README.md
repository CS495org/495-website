# Proxy

```
Compose service name: nginx
Container name: tv-proxy
Base image: nginx:alpine
Relevant .env variables: N/A
Function: Handle ingress, serve static assets
```

This directory is for the NGINX reverse proxy. This container handles incoming requests, forwarding them to the web container and serving static assets. In development, self signed TLS certs are generated on the fly inside this container. In production, persistent certificates endorsed by a CA are mounted inside the container.

Static assets relating to the structure of the site are stored here in the "static" directory (things like icons, buttons, CSS and JS files). Movie and show posters and backdrops are stored in the img-var volume, which is mounted in this container. These JPG files are pulled down by a celery app running in the web container, but are served by the proxy in this container.

This service runs on the frontend network. Do not attach the backend network.