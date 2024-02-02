# CS 495 Website
Hi this is the website

If you're a collaborator on this, please scroll to the bottom for repo stuff

## Run the Website

First, make a .env file. Copy the format from .env.example. Use single quotes if any env vars have $ or @ or other characters that can mess with a shell.

```docker compose up --build```

Give it a minute to build, Django app waits for redis start and DB healthcheck, then has to make/migrate, then reverse proxy starts.

don't forget ```docker compose down``` after you're done.

To remove Docker volumes (postgres volume enabled by default, redis volume disabled by default):

```docker volume rm 495-website_pg-data```

```docker volume rm 495-website_redis-data```

## Test it

https://localhost/

It'll warn you that the certificate isn't verified, right now it's being generated on the fly at runtime, don't worry about it.

Still need to bump docs on https stuff, but the gist is that the NGINX container is generating certs on the fly, fine for development, obviously not gonna work for production, I'll generate real certs registered with CA and mount from compose (or, more likely, copy from the Dockerfile), along with DH param.

To test Database:

```curl -k https://localhost/db-test-endpt/```

To test Redis:

```curl -k https://localhost/redis-test-endpt/```

You have to add the -k flag for now to make cURL bypass certificate validation

If you make requests with python, add verify=False to the API call


## Run the whole thing

We're using Airbyte for ELT. If you want to run Airbyte on your machine along with the web app:

(from this directory, because it's using relative paths): ```./dothestuff.sh```

If you have an older computer and/or a slower network connection, it could take a while for Airbyte to start up. Go to the dothestuff script to run the containers detached and allow Airbyte to attach STDOUT.

This will create a sibling directory with our fork of Airbyte and start it up. I'm suppressing output by default because watching my CLI start up Airbyte and this project at the same time nearly gave me a seizure. 

After startup, Airbyte will be available at http://localhost:8000/. Default user: "airbyte". Default password: "password". You can change those in the .env in the airbyte directory.

Don't worry about the registration, you can just put "email@email.com" for your email and "NA" for your organization. Or give them your real info, makes no difference to me.

To stop Airbyte, just docker compose down from ../airbyte.


## Tech stack

Web app backend: Django

Server: Gunicorn

Reverse proxy: NGINX

Containerization: Docker/compose

Database: Postgres

Cache/Message Broker: Redis

ELT: Airbyte


## Repo stuff

I'm just making everyone their own branch for now. We'll probably end up with dev-stable and dev-latest branches as well, but for now this is fine. When you push commits, please don't just ```git push```

Instead: ```git push origin <YOUR_NAME>```

Same goes for pull, unless you're trying to pull a different branch

If you clone the wrong branch: ```git checkout <BRANCH_NAME>```

I'm trying to figure out branch protection rules without signing up for an enterprise account, maybe I'll figure it out, we'll see

Please please please don't force push. If you *have* to force to your own branch, sure, but if you force push to main then we'd all better hope that someone has it backed up somewhere, which I'm not planning on doing