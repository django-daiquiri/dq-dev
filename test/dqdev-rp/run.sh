#!/bin/bash

name="dqdev-rp"

docker build --tag ${name} .
docker run -d \
    --name ${name} \
    -p 443:443 \
    ${name}

docker network connect dqdevnet_test ${name}
