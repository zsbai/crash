#!/bin/bash

echo "getting latest version"
latest_version=`curl -s "https://api.bailu.workers.dev/repos/Dreamacro/clash/releases/latest"|grep "tag_name"|head -n 1|awk -F ":" '{print $2}'|sed 's/\"//g;s/,//g;s/ //g'`;
echo "clash latest version is ${latest_version}"

echo "Downloading clash..."
if command -v arch >/dev/null 2>&1; then
	platform=`arch`
else
	platform=`uname -m`
fi

if [ "$platform" = "x86_64" ];then
    ARCH=amd64
    NODEJSARCH=x64
elif [ "$platform" = "aarch64" ];then
    ARCH=arm64
fi

wget https://gh-proxy.bailu.workers.dev/Dreamacro/clash/releases/download/${latest_version}/clash-$(uname -s| tr [:upper:] [:lower:])-${ARCH}-${latest_version}.gz -O clash.gz
if command -v gzip > /dev/null 2>&1; then
    gzip -d clash.gz
else
    apt-get install gzip -y
    gzip clash.gz
fi
mv clash /usr/local/bin/clash
chmod +x /usr/local/bin/clash

clash -v
echo "clash installed"

echo "create systemd"
cat >/etc/systemd/system/clash.service <<EOF
[Unit]
Description=clash daemon

[Service]
Type=simple
ExecStart=/usr/bin/clash -d $(pwd ~)/.config/clash/
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable clash
echo "systemd created"