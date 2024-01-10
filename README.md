[![Docker Image CI](https://github.com/HFxLhT8JqeU5BnUG/495-website/actions/workflows/docker-compose-test.yml/badge.svg)](https://github.com/HFxLhT8JqeU5BnUG/495-website/actions/workflows/docker-compose-test.yml)

```git clone https://github.com/HFxLhT8JqeU5BnUG/495-website.git```

```cd 495-website```

```sudo docker compose up --build```

don't forget ```sudo docker compose down``` after you're done

http://localhost:443/

**Not** HTTPS


To test JSONReponse/Database:

```curl localhost:443/db_test_endpt/```


Tech stack:

Web app backend: Django

Server: Gunicorn

Reverse proxy: NGINX

Containerization: Docker/Docker compose

Database: Postgres