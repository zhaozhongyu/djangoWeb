#!/bin/bash
if [ -f /etc/SuSE-release ]; then
    suse11=`cat /etc/SuSE-release | grep 'VERSION = 11'`
    if [[ -n ${suse11} ]];then
        rcntp start;
    else
        service ntpd start;
    fi
else
    service ntpd start
fi
