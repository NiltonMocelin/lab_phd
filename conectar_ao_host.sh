#!/bin/bash
echo 'uso bash conectar_ao_host.sh "-p porta user@ip_do_host"'
sudo chmod 600 chave_lab
ssh -i chave_lab $1
