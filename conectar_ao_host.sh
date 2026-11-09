#!/bin/bash
echo "uso bash conectar_ao_host.sh <ip_do_host>"
sudo chmod 755 chave_lab/chave_lab
ssh -i chave_lab/chave_lab niltonm@$1
