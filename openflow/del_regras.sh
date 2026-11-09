#!/bin/bash
echo "[dentro do host] uso: bash del_regras.sh <ip_do_switch> <ip_do_destino>"
IPSWITCH=$1
IPDESTINO=$2
sudo ovs-ofctl -O OpenFlow13 del-flows tcp:$IPSWITCH:6653 "nw_dst=$IPDESTINO"