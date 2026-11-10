
echo Modo de uso bash iniciar_background.sh <ip_do_host>
nohup iperf3 -c $1 -u -B 15M > iperf3.log 2>&1 &