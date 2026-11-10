echo "Configurando host 4"
sudo apt-get update

sudo apt install -y openvswitch-switch

sudo apt install -y python3-pip
python3 -m pip install pysflow

sudo sysctl -w net.ipv4.neigh.default.base_reachable_time_ms=3600000

INTERFACE=$(ip -o addr show | awk '/inet 192\.168\./ {print $2; exit}')
sudo ip link set dev "$INTERFACE" down
sleep 1
sudo ip link set dev $INTERFACE address 00:00:00:00:04:01
sudo ip link set dev $INTERFACE up

echo "Configurando ARP estático para o switch"
sudo arp -s 192.168.4.1 00:00:00:00:04:02

sudo apt-get install -y openvswitch-common
sudo apt-get install -y iperf3
nohup iperf3 -s > iperf3.log 2>&1 &
sudo apt install ffmpeg -y