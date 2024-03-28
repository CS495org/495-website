# FROM python:3.12-alpine3.19
FROM localhost:5000/website
# if you have a personal registry set up

ARG USER
ARG PASSWORD
ARG HOST
ARG PORT
ARG DATABASE
ARG DJANGO_USER
ARG DJANGO_SECURE_KEY
ARG DJANGO_PG_SCHEMA

# env vars plugged in at runtime, not at build, so using ARGs here

ENV USER $USER
ENV PASSWORD $PASSWORD
ENV HOST $HOST
ENV PORT $PORT
ENV DJANGO_USER $DJANGO_USER
ENV DJANGO_SECURE_KEY $DJANGO_SECURE_KEY
ENV DJANGO_PG_SCHEMA $DJANGO_PG_SCHEMA

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# need to make/migrate
ENTRYPOINT [ "./startup.sh" ]