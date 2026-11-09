echo "Configurando switch 10"
echo "substituir HIP pelo ip do host"
HIP=192.168.10.2
HMAC=00:00:00:00:0A:01
SNET=1

HINTERFACE=$(ip -o addr show | awk '/inet 192\.168\.10\./ {print $2; exit}')
S1INTERFACE=$(ip -o addr show | awk '/inet 192\.168\.1\./ {print $2; exit}')
S2INTERFACE=$(ip -o addr show | awk '/inet 192\.168\.2\./ {print $2; exit}')
S3INTERFACE=$(ip -o addr show | awk '/inet 192\.168\.3\./ {print $2; exit}')
S4INTERFACE=$(ip -o addr show | awk '/inet 192\.168\.4\./ {print $2; exit}')
S5INTERFACE=$(ip -o addr show | awk '/inet 192\.168\.5\./ {print $2; exit}')
S6INTERFACE=$(ip -o addr show | awk '/inet 192\.168\.6\./ {print $2; exit}')
S7INTERFACE=$(ip -o addr show | awk '/inet 192\.168\.7\./ {print $2; exit}')
S8INTERFACE=$(ip -o addr show | awk '/inet 192\.168\.8\./ {print $2; exit}')
S9INTERFACE=$(ip -o addr show | awk '/inet 192\.168\.9\./ {print $2; exit}')

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
sudo ovs-vsctl add-port switch1 $S1INTERFACE -- set interface $S1INTERFACE ofport_request=2
sudo ovs-vsctl add-port switch1 $S2INTERFACE -- set interface $S2INTERFACE ofport_request=3
sudo ovs-vsctl add-port switch1 $S3INTERFACE -- set interface $S3INTERFACE ofport_request=4
sudo ovs-vsctl add-port switch1 $S4INTERFACE -- set interface $S4INTERFACE ofport_request=5
sudo ovs-vsctl add-port switch1 $S5INTERFACE -- set interface $S5INTERFACE ofport_request=6
sudo ovs-vsctl add-port switch1 $S6INTERFACE -- set interface $S6INTERFACE ofport_request=7
sudo ovs-vsctl add-port switch1 $S7INTERFACE -- set interface $S7INTERFACE ofport_request=8
sudo ovs-vsctl add-port switch1 $S8INTERFACE -- set interface $S8INTERFACE ofport_request=9
sudo ovs-vsctl add-port switch1 $S9INTERFACE -- set interface $S9INTERFACE ofport_request=10

echo "configurando sFlow"
sudo ovs-vsctl -- --id=@s create sflow agent=eno2 targets="$HIP:6343" sampling=64 poll=10 \ -- set bridge switch1 sflow=@s

echo "configurando as regras de fluxo"
sudo ovs-ofctl add-flow switch1 "ip,nw_dst=192.168.10.2,actions=set_field:eth_dst->$HMAC,output:1"
sudo ovs-ofctl add-flow switch1 "ip,nw_dst=192.168.1.0/24,actions=output:2"
sudo ovs-ofctl add-flow switch1 "ip,nw_dst=192.168.2.0/24,actions=output:3"
sudo ovs-ofctl add-flow switch1 "ip,nw_dst=192.168.3.0/24,actions=output:4"
sudo ovs-ofctl add-flow switch1 "ip,nw_dst=192.168.4.0/24,actions=output:5"
sudo ovs-ofctl add-flow switch1 "ip,nw_dst=192.168.5.0/24,actions=output:6"
sudo ovs-ofctl add-flow switch1 "ip,nw_dst=192.168.6.0/24,actions=output:7"
sudo ovs-ofctl add-flow switch1 "ip,nw_dst=192.168.7.0/24,actions=output:8"
sudo ovs-ofctl add-flow switch1 "ip,nw_dst=192.168.8.0/24,actions=output:9"
sudo ovs-ofctl add-flow switch1 "ip,nw_dst=192.168.9.0/24,actions=output:10"