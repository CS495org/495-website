#!/bin/bash

docker compose down && docker volume rm 495-website_pg-data #&& docker volume rm 495-website_redis-data
docker compose up --build --force-recreate --remove-orphans