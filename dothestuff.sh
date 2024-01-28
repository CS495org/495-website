#!/bin/bash

env_file=".env"

if [ -f "$env_file" ]; then
    source "$env_file"
else
    echo "You forgot the .env" && exit
fi

# no need to .env this
local_repo_path="../airbyte"

# check for repo
if [ -d "$local_repo_path" ]; then
    # If exists, pull
    cd ".."
    git pull
else
    # else clone
    cd ".."
    git clone "$OUR_AIRBYTE"
fi


cd "airbyte"
./run-ab-platform.sh > /dev/null 2>&1 &
# If you're having problems with airbyte, put a # before the ">"

cd "../495-website"
docker compose up --build