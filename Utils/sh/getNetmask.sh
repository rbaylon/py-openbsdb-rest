#!/bin/ksh

#
# Get interface ip netmask
#

iface=$1
ip=$2

if [[ "${iface}x" != "x" ]];then
    ifconfig $iface >/dev/null 2>&1
    if [[ $? -ne 0 ]];then
        exit 2
    fi
else
    exit 1
fi

. `dirname $0`/common.sh

nm=`ifconfig $iface | grep $ip | awk '{print $4}'`
hex2ip $nm
