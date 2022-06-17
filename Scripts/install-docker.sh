#!/bin/bash

echo " Installing docker using official script..."

if [ ! "$(command -v curl)" ]; then
  apt-get update && apt-get install sudo curl wget vim ca-certificates -y
fi

curl -fsSL get.docker.com -o get-docker.sh | sh get-docker.sh

docker -v
echo "Docker installed"