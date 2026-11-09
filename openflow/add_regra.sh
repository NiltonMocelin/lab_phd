#!/bin/bash
echo "[dentro do host] uso: bash add_regra.sh <ip_do_switch> <ip_do_destino> <mac_do_destino> <porta>"
sudo ovs-ofctl -OOpenFlow13 add-flow tcp:$1:6653 "priority=100,ip,nw_dst=$2,actions=set_field:eth_dst->$3,output:$4"