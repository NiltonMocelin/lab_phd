echo "Configurando switch 1"
echo "substituir HIP pelo ip do host"
HIP=192.168.1.2
HMAC=00:00:00:00:01:01
SMAC=00:00:00:00:01:02
SNET=1

HINTERFACE=$(ip -o addr show | awk '/inet 192\.168\.1\.1/ {print $2; exit}')
SINTERFACE=$(ip -o addr show | awk '/inet 192\.168\.1\.3/ {print $2; exit}')

sudo ip link set dev "$HINTERFACE" down
sleep 1
sudo ip link set dev $HINTERFACE address $SMAC
sudo ip link set dev $HINTERFACE up

sudo arp -s $HIP $HMAC

echo "Instalando dependencias"
sudo apt-get update
sudo apt-get install -y openvswitch-switch
sudo systemctl enable --now openvswitch-switch

echo "Criando o switch OVS e configurando"
sudo ovs-vsctl add-br switch1
sudo ovs-vsctl set bridge switch1 protocols=OpenFlow13
sudo ovs-vsctl show

sudo ovs-vsctl set bridge switch1 other-config:datapath-id=0000000000000001
sudo ovs-vsctl set-controller switch1 tcp:$HIP:6653 
sudo ovs-vsctl set Bridge switch1 fail-mode=secure

echo "Adicionando portas ao switch"
sudo ovs-vsctl add-port switch1 $HINTERFACE -- set interface $HINTERFACE ofport_request=1
sudo ovs-vsctl add-port switch1 $SINTERFACE -- set interface $SINTERFACE ofport_request=2

echo "configurando sFlow"
sudo ovs-vsctl -- --id=@s create sflow agent=$HINTERFACE targets="[\"$HIP:6343\"]" sampling=64 poll=10 -- set bridge switch1 sflow=@s

echo "configurando as regras de fluxo"
sudo ovs-ofctl -OOpenFlow13 add-flow switch1 "priority=100,ip,nw_dst=192.168.1.2,actions=set_field:$HMAC->eth_dst,output:1"
sudo ovs-ofctl -OOpenFlow13 add-flow switch1 "priority=10,ip,nw_dst=192.168.0.0/16,actions=output:2"