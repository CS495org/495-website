[![Docker Image CI](https://github.com/HFxLhT8JqeU5BnUG/495-website/actions/workflows/docker-compose-test.yml/badge.svg)](https://github.com/HFxLhT8JqeU5BnUG/495-website/actions/workflows/docker-compose-test.yml)

```git clone https://github.com/HFxLhT8JqeU5BnUG/495-website.git```

```cd 495-website```

```sudo docker compose up --build```

don't forget ```sudo docker compose down``` after you're done

To remove Docker volumes (postgres volume enabled by default, redis volume disabled by default)

```sudo docker volume rm 495-website_postgres-data```

```sudo docker volume rm 495-website_redis-data```

http://localhost:443/

Not HTTPS, no point in configuring SSL/TLS until first deployment

To test JSONReponse/Database:

```curl localhost:443/db-test-endpt/```

To test Redis:

```curl localhost:443/redis-test-endpt/```


Tech stack:

Web app backend: Django

Server: Gunicorn

Reverse proxy: NGINX

Containerization: Docker/Docker compose

Database: Postgres

Key-Value Store/Message Broker: Redis