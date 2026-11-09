#!/bin/bash
echo "[dentro do host] uso: bash listar_switches.sh <ip_do_switch>"
sudo ovs-vsctl --db=tcp:$1:6640 list-br