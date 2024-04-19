# Database

```
Compose service name: db
Container name: tv-db
Base image: postgres:16-alpine3.19
Relevant .env variables:
    POSTGRES_USER
    POSTGRES_PASSWORD
    POSTGRES_DB
    HOST
    PORT
Function: Storage for Django backend, Airbyte TMDB data
```


This directory is for anything related to our postgres database. In development, we use the (now zipped) init-2.sql file to fill realistic but static data. No ports need to be exposed in development, but it helps if you want to check out the database. In production, some host port needs to be bound to 5432 (or whatever port you want the database to run on inside the container) for Airbyte to drop TMDB data to.

If you want to use the init-2.sql sample data, use "tate" as both the POSTGRES_USER and POSTGRES_DB env variables. There's no built in way to use env variables in a .sql file, so when I pulled down the sample data with pg dump, it hardcoded those values. Obviously we won't be mounting a startup .sql script in production, but if you get any kind of database errors in development, make sure that you have those variables set correctly and you aren't using the pg-data volume to persist a depreciated database structure/authentication.

This container runs on the "backend" network and has two potential volumes. The init-2.sql file can be mounted to initialize the database, and the pg-data volume is mounted to handle the persistent storage of data. Do not attach it to the frontend network- separate networks ensure that the web container stands between incoming web requests and the actual data.