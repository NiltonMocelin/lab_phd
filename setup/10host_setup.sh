echo "Configurando host 10 - server"

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

INTERFACE=$(ip -o addr show | awk '/inet 192\.168\.10\./ {print $2; exit}')
sudo ip link set dev "$INTERFACE" down
sleep 1
sudo ip link set dev $INTERFACE address 00:00:00:00:0A:01
sudo ip link set dev $INTERFACE up

sudo apt-get update
sudo apt-get install -y openvswitch-common
sudo apt-get install iperf3

# Baixa o pacote compactado (substitua a versão se necessário)
echo instalando mediamtx
wget https://github.com/bluenviron/mediamtx/releases/download/v1.21.3/mediamtx_v1.21.3_linux_amd64.tar.gz
# curl -L -O https://github.com/bluenviron/mediamtx/releases/download/v1.21.3/mediamtx_v1.21.3_linux_amd64.tar.gz
tar -xvzf mediamtx_v1.21.3_linux_amd64.tar.gz
nohup ./mediamtx > mediamtx.log 2>&1 &