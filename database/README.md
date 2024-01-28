Leaving init.sql here for testing for now.

Uncomment port binding in docker compose file to access database from host machine

Using host port 4567 to avoid collisions with any existing locally hosted postgres database

Docker allocates the virtual network automatically, so to get the IP address of the database host:

```docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 495-db```

To look at the results of the test-db-endpt view, run (from host machine):

```curl -k https://localhost/db-test-endpt/```


To delete the Docker volume that holds the postgres data:

```docker volume rm 495-website_pg-data```