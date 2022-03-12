#!/usr/bin/env bash

TAG=${1:-latest}

docker pull aspin/fwordle-backend:${TAG}
docker rm -f fwordle-backend
docker run -d -p 9000:9000 --name fwordle-backend aspin/fwordle-backend:${TAG}
