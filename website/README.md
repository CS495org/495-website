# Web App

```
Compose service name: web
Container name: tv-web
Base image: python3.12-alpine
Relevant .env variables:
    POSTGRES_USER
    POSTGRES_PASSWORD
    POSTGRES_DB
    HOST
    PORT

    DJANGO_SECURE_KEY
    DJANGO_USER
    DJANGO_PG_SCHEMA

    RHOST
    RPORT

    GMAIL
    GMAILPSWD

    TMDB_API_KEY

Function: Serve Django web app logic over a gunicorn server, along with the celery task queue
```


This directory is for the core functionality of the whole project. It contains the Django web application. The project directory is ./project. Installed apps are "accounts" and "our_app." The templates directory is for the HTML Django templates. The interfaces directory is for reusable interfaces that interact with containers/services external to the web application (postgres and redis).

Accounts contains our TV show, movie, and user models,