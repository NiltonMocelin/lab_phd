import socket
import threading
import time
import subprocess
from collections import defaultdict
import sflow  # Biblioteca pysflow para decodificar o sFlow binário (pip install pysflow)

# --- CONFIGURAÇÕES DE REDE E OPENFLOW ---
SWITCH_TARGET = "tcp:192.168.1.1:6643"  # IP e porta PTCP do switch1
METER_ID = 1
RATE_KBPS = 500                        # Limite de banda imposto pelo Meter (kbps)
SAMPLING_RATE = 64                     # Taxa de amostragem configurada no OVS (sampling=64)
SO_MOSTRAR = True                      # True = apenas simula/loga; False = aplica a regra no OVS

# Dicionário global para acumular os fluxos em memória
active_flows = defaultdict(int)
lock = threading.Lock()

def parse_sflow_packets(decoded_data):
    """
    Percorre o dicionário gerado pelo pysflow.decode() para extrair 
    IPs, portas, protocolo e calcular o volume real de bytes.
    """
    extracted_flows = []
    try:
        samples = decoded_data.get('samples', [])
        for sample in samples:
            # Processamos apenas amostras de fluxo (FlowSamples)
            if sample.get('sample_type') == 'flow':
                records = sample.get('elements', []) or sample.get('flow_records', [])
                
                src_ip, dst_ip, proto, src_port, dst_port, pkt_len = None, None, "0", "0", "0", 0
                
                for record in records:
                    header = record.get('header') or record.get('sampled_header')
                    if header:
                        pkt_len = header.get('frame_length', 100)
                        
                        # Camada de Rede (IP)
                        ip_layer = header.get('ip') or header.get('ipv4')
                        if ip_layer:
                            src_ip = str(ip_layer.get('src'))
                            dst_ip = str(ip_layer.get('dst'))
                            proto = str(ip_layer.get('proto', '0'))
                            
                        # Camada de Transporte (TCP / UDP)
                        tp_layer = header.get('tcp') or header.get('udp')
                        if tp_layer:
                            src_port = str(tp_layer.get('sport') or tp_layer.get('source_port', '0'))
                            dst_port = str(tp_layer.get('dport') or tp_layer.get('destination_port', '0'))
                
                if src_ip and dst_ip:
                    # Reconstrói o volume real multiplicando pelo fator de amostragem do OVS
                    estimated_bytes = pkt_len * SAMPLING_RATE
                    extracted_flows.append((src_ip, dst_ip, proto, src_port, dst_port, estimated_bytes))
                    
    except Exception:
        pass
    return extracted_flows

def sflow_socket_listener():
    """
    Abre um socket UDP nativo no host1 para escutar diretamente a porta 6343
    enviada pelo switch1.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind(("0.0.0.0", 6343))
        print("[*] Coletor sFlow RAW com pysflow ouvindo na porta UDP 6343...")
    except Exception as e:
        print(f"[-] Erro ao abrir socket na porta 6343: {e}")
        return

    while True:
        try:
            data, addr = sock.recvfrom(65535)
            
            # Decodifica o datagrama binário bruto usando a lib pysflow
            decoded = sflow.decode(data)
            
            # Extrai os fluxos estruturados
            flows_extracted = parse_sflow_packets(decoded)
            
            # Agrega no dicionário global thread-safe
            for src_ip, dst_ip, proto, src_port, dst_port, pkt_bytes in flows_extracted:
                flow_key = (src_ip, dst_ip, proto, src_port, dst_port)
                with lock:
                    active_flows[flow_key] += pkt_bytes
                    
        except Exception as e:
            # Ignora erros de pacotes corrompidos ou malformados na rede
            continue

def get_top_flows():
    """Retorna os fluxos ordenados por maior volume de bytes na janela"""
    with lock:
        sorted_flows = sorted(active_flows.items(), key=lambda x: x[1], reverse=True)
        top = sorted_flows[:10]
        active_flows.clear()  # Reseta o acumulador para a próxima janela
    return top

if __name__ == "__main__":
    # Inicia a thread de escuta UDP em background
    listener_thread = threading.Thread(target=sflow_socket_listener, daemon=True)
    listener_thread.start()
    
    print(f"[*] Gerenciador SDN (Método RAW + pysflow) rodando no host1. Controlando switch ({SWITCH_TARGET})...")
    
    # Loop principal de análise de tráfego a cada 5 segundos
    while True:
        time.sleep(5)
        top_flows = get_top_flows()
        
        if top_flows:
            print(f"\n--- [Janela de Análise] Top {len(top_flows)} fluxos ---")
            for flow_key, total_bytes in top_flows:
                src_ip, dst_ip, proto, src_port, dst_port = flow_key
                print(f"  -> Origem: {src_ip}:{src_port} | Destino: {dst_ip}:{dst_port} | Proto: {proto} | Bytes Estimados: {total_bytes}")
                
                # Heurística de fluxo ganancioso (> 10 MB acumulados na janela)
                if total_bytes > 10_000_000:
                    print(f"[!] FLUXO GANANCIOSO IDENTIFICADO! IP: {src_ip}:{src_port}")