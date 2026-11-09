echo "Modo de uso bash acessar_streaming.sh <ip_do_servidor> <ip_do_host>"
echo "[*] Para acessar o streaming, use o comando SSH com tunelamento reverso:"
echo "ssh -L 8888:<ip_do_servidor>:8888 usuario@<ip_do_host>"
ssh -L 8888:$1:8888 usuario@$2

echo "[*] Depois, abra o navegador e acesse: http://localhost:8888/stream/"