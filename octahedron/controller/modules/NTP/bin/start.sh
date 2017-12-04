#!/bin/bash
cd $(dirname ${BASH_SOURCE[0]});
source ../module.conf
sleep ${starttime};
if [ -f /etc/SuSE-release ]; then
    suse11=`cat /etc/SuSE-release | grep 'VERSION = 11'`
    if [[ -n ${suse11} ]];then
        rcntp stop;
    else
        service ntpd stop;
    fi
else
    service ntpd stop
fi
#环境上必须要设定一个睡眠暂停时间
sleep ${duration};
sh stop.sh
