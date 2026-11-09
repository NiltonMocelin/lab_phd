#!/bin/bash
echo "[dentro do host] uso: bash list_meter.sh <ip_do_switch>"
sudo ovs-ofctl -OOpenFlow13 dump-meters tcp:$1:6653