FROM docker:25-dind

RUN apk --update add --no-cache git bash curl

RUN git clone --depth=1 https://github.com/HFxLhT8JqeU5BnUG/airbyte.git


ENTRYPOINT [ "bash /airbyte/run-ab-platform.sh" ]