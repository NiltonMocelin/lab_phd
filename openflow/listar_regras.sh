#!/bin/bash
echo "[dentro do host] uso: bash add_meter.sh <ip_do_switch>"
sudo ovs-ofctl -OOpenFlow13 dump-flows tcp:$1:6653