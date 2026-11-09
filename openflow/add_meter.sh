#!/bin/bash
echo "[dentro do host] uso: bash add_meter.sh <ip_do_switch> <METER_ID> <RATE_KBPS>"
sudo ovs-ofctl -OOpenFlow13 add-meter tcp:$1:6653 "meter=$2,kbps,band=type=drop,rate=$3"