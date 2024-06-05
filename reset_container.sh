#!/bin/bash

docker stop $(docker ps -q)
docker rm $(docker ps -aq)
docker build -t simple-knowledge-sharing-platform .
docker run -d -p 8080:5000 -v $(pwd)/uploads:/app/uploads simple-knowledge-sharing-platform
