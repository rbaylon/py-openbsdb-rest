#!/bin/ksh

hex2ip()
{
    h=$1
    printf '%d.%d.%d.%d' $(echo ${h#0x} | sed 's/../0x& /g')
}
