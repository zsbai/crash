#!/bin/bash

echo "getting latest version.."
latest_version=`curl -s "https://api.github.com/repos/docker/compose/releases/latest"|grep "tag_name"|head -n 1|awk -F ":" '{print $2}'|sed 's/\"//g;s/,//g;s/ //g'`;
echo "docker-compose latest release version is ${latest_version}"
echo "downloading..."
wget https://github.com/docker/compose/releases/download/${latest_version}/docker-compose-$(uname -s)-$(uname -m) -O /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker-compose -v
echo "\e[1;31m docker-compose installed \e[0m"