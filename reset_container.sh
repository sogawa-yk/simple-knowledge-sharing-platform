#!/bin/bash

docker build -t simple-knowledge-sharing-platform .
docker run -d -p 8080:5000 --network flask-net -v $(pwd)/uploads:/app/uploads simple-knowledge-sharing-platform
