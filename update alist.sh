date=`date`
echo "脚本执行时间：${date}"
# myip=`curl -s cip.cc|grep IP|awk -F ":" '{print $2}'|sed 's/ //g'`
platform=`uname -m`

if [ "$platform" = "x86_64" ];then
    ARCH=amd64
    NODEJSARCH=x64
elif [ "$platform" = "aarch64" ];then
    ARCH=arm64
    NODEJSARCH=arm64
    GLIBC_VERSION=`ldd --version|grep ldd|grep -oP '\) \K.*'|awk -F. '{print $2}'`
    if [[ ! "$GLIBC_VERSION" -ge "28" ]];then
        echo -e "\r\n${RED_COLOR}出错了${RES}，ARM64 架构要求 glibc 版本 ${GREEN_COLOR}≥ 2.28${RES}，当前 glibc 版本：${GREEN_COLOR}2.$GLIBC_VERSION${RES}"
        echo -e "ARM64 架构建议更换 Debian & Ubuntu 操作系统再试\r\n"
        exit 1;
    fi
fi
#检查alist是否安装在/opt/
if [ ! -d "/opt/alist-v2/" ];then
  echo
  echo "alist not install in /opt/"
  echo
  exit 1:
fi

echo -e "\033[36m获取 Alist 版本信息 ...\033[0m"


latest_version2=`curl -s "https://api.github.com/repos/alist-org/alist/releases/latest"|grep "tag_name"|head -n 1|awk -F ":" '{print $2}'|sed 's/\"//g;s/,//g;s/ //g'`;

echo -e "\r\n下载 Alist $latest_version2 ..."

systemctl stop alist

curl -L https://gh-proxy.baiblog.ren/alist-org/alist/releases/download/$latest_version2/alist-linux-$ARCH.tar.gz -o /opt/alist-v2/alist.tar.gz
tar zxf /opt/alist-v2/alist.tar.gz -C /opt/alist-v2/
mv /opt/alist-v2/alist-linux-$ARCH /opt/alist-v2/alist

rm -f /opt/alist-v2/alist.tar.gz

chmod +x /opt/alist-v2/alist
systemctl start alist
