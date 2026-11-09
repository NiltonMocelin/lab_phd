
echo Modo de uso bash iniciar_background.sh <ip_do_host>
nohup iperf3 -c -u -B 15M $1 > iperf3.log 2>&1 &