#!/bin/sh

docker compose down && docker volume rm 495-website_pg-data #&& docker volume rm img-var
docker volume create img-var
docker compose up --build --force-recreate --remove-orphans # -d