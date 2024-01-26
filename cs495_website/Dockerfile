FROM python:3.12-slim


ARG USER
ARG PASSWORD
ARG HOST
ARG PORT
ARG DATABASE
ARG DJANGO_USER
ARG DJANGO_SECURE_KEY

# env vars plugged in at runtime, not at build, so using ARGs here

ENV USER $USER
ENV PASSWORD $PASSWORD 
ENV HOST $HOST 
ENV PORT $PORT 
ENV DJANGO_USER $DJANGO_USER 
ENV DJANGO_SECURE_KEY $DJANGO_SECURE_KEY 

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod ugo+rwx ./startup.sh

# need to make/migrate
ENTRYPOINT [ "./startup.sh" ]