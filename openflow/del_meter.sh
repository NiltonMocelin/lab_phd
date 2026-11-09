echo "[dentro do host] uso: bash del_meter.sh <ip_do_switch> <METER_ID>"
IPSWITCH=$1
METER_ID=$2
sudo ovs-ofctl -OOpenFlow13 del-meter tcp:$IPSWITCH:6653 "meter=$METER_ID"