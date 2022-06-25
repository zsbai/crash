#!/bin/bash

echo "getting latest version.."
latest_version=`curl -s "https://api.github.com/repos/git-lfs/git-lfs/releases/latest"|grep "tag_name"|head -n 1|awk -F ":" '{print $2}'|sed 's/\"//g;s/,//g;s/ //g'`;
echo "git-lfs latest release version is ${latest_version}"
echo "downloading..."
if command -v arch >/dev/null 2>&1; then
	platform=`arch`
else
	platform=`uname -m`
fi

if [ "$platform" = "x86_64" ];then
    ARCH=amd64
elif [ "$platform" = "aarch64" ];then
    ARCH=arm64
fi

wget https://github.com/git-lfs/git-lfs/releases/download/${latest_version}/git-lfs-$(uname -s| tr [:upper:] [:lower:])-${ARCH}-${latest_version}.zip -O lfs.zip
mkdir ./lfs
tar -zxvf lfs.tar.gz -C ./lfs
cd lfs && sh install.sh
echo "git-lfs installed"
rm -f lfs.tar.gz