#!/bin/bash
echo "[dentro do host] uso: bash bloquear_fluxo.sh <ip_do_switch> <ip_do_destino>"
IPSWITCH=$1
IPDESTINO=$2
sudo ovs-ofctl -OOpenFlow13 add-flow tcp:$IPSWITCH:6653 "priority=100,ip,nw_dst=$IPDESTINO,actions=drop"