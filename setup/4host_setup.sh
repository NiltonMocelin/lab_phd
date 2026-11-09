echo "Configurando host 4"
sudo apt-get update
# sudo pip3 install ryu
sudo apt install openvswitch-switch

# echo "Installing sFlow-RT"
# wget https://inmon.com/products/sFlow-RT/sflow-rt.tar.gz
# tar -xvzf sflow-rt.tar.gz
# cd sflow-rt
# ./start.sh

pip install pysflow

sudo sysctl -w net.ipv4.neigh.default.base_reachable_time_ms=3600000

INTERFACE=$(ip -o addr show | awk '/inet 192\.168\./ {print $2; exit}')
sudo ip link set dev "$INTERFACE" down
sleep 1
sudo ip link set dev $INTERFACE address 00:00:00:00:04:01
sudo ip link set dev $INTERFACE up


sudo apt-get update
sudo apt-get install -y openvswitch-common
sudo apt-get install iperf3
nohup iperf3 -s -u > iperf3.log 2>&1 &