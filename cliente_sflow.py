import socket
import threading
import time
from collections import defaultdict
import sflow

LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 6343
SAMPLING_RATE = 10  # Taxa de amostragem configurada no OVS

active_flows = defaultdict(int)
lock = threading.Lock()

def parse_hex_header(header_hex):
    """
    Converte a string hexadecimal do cabeçalho bruto e extrai 
    IP de origem, IP de destino, protocolo, portas e tamanho do pacote.
    """
    try:
        b = bytes.fromhex(header_hex)
        ip_start = -1
        
        # Procura o início do cabeçalho IPv4 (versão 4, IHL >= 5)
        for i in range(len(b) - 20):
            if (b[i] & 0xF0) == 0x40:  # Versão 4
                ihl = b[i] & 0x0F
                if ihl >= 5 and i + 20 <= len(b):
                    proto = b[i + 9]
                    if proto in (6, 17, 1):  # TCP, UDP, ICMP
                        ip_start = i
                        break
        
        if ip_start != -1:
            ihl = (b[ip_start] & 0x0F) * 4
            total_len = int.from_bytes(b[ip_start+2:ip_start+4], 'big')
            proto = b[ip_start+9]
            
            # IPs de Origem e Destino
            src_ip = f"{b[ip_start+12]}.{b[ip_start+13]}.{b[ip_start+14]}.{b[ip_start+15]}"
            dst_ip = f"{b[ip_start+16]}.{b[ip_start+17]}.{b[ip_start+18]}.{b[ip_start+19]}"
            
            src_port, dst_port = "0", "0"
            transport_start = ip_start + ihl
            
            # Portas TCP ou UDP
            if proto in (6, 17) and transport_start + 4 <= len(b):
                src_port = str(int.from_bytes(b[transport_start:transport_start+2], 'big'))
                dst_port = str(int.from_bytes(b[transport_start+2:transport_start+4], 'big'))
                
            return src_ip, dst_ip, str(proto), src_port, dst_port, total_len
            
    except Exception:
        pass
        
    return None, None, "0", "0", "0", 100

def parse_sflow_packets(decoded_data):
    extracted_flows = []
    try:
        samples = decoded_data.get('samples', [])
        for sample in samples:
            records = sample.get('flow_records', []) or sample.get('elements', [])
            for record in records:
                header = record.get('header')
                if isinstance(header, str):
                    src_ip, dst_ip, proto, src_port, dst_port, pkt_len = parse_hex_header(header)
                    if src_ip and dst_ip and src_ip != "0.0.0.0":
                        estimated_bytes = pkt_len * SAMPLING_RATE
                        extracted_flows.append((src_ip, dst_ip, proto, src_port, dst_port, estimated_bytes))
                        
    except Exception as e:
        print(f"[-] Erro no parsing: {e}")
        
    return extracted_flows

def sflow_socket_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((LISTEN_IP, LISTEN_PORT))
    print(f"[*] Coletor sFlow a escutar em {LISTEN_IP}:{LISTEN_PORT}...")

    while True:
        try:
            data, addr = sock.recvfrom(65535)
            decoded = sflow.decode(data)
            
            flows_extracted = parse_sflow_packets(decoded)
            for src_ip, dst_ip, proto, src_port, dst_port, pkt_bytes in flows_extracted:
                flow_key = (src_ip, dst_ip, proto, src_port, dst_port)
                with lock:
                    active_flows[flow_key] += pkt_bytes
        except Exception:
            continue

if __name__ == "__main__":
    threading.Thread(target=sflow_socket_listener, daemon=True).start()
    
    print("[*] Sistema de análise de top flows operacional. Gere tráfego (iperf/ping)...")
    
    try:
        while True:
            time.sleep(5)
            with lock:
                if active_flows:
                    print(f"\n--- [Janela de Análise] Top Fluxos ---")
                    sorted_flows = sorted(active_flows.items(), key=lambda x: x[1], reverse=True)
                    for flow_key, total_bytes in sorted_flows[:10]:
                        s_ip, d_ip, pr, s_p, d_p = flow_key
                        print(f"  Origem: {s_ip}:{s_p} -> Destino: {d_ip}:{d_p} | Proto: {pr} | Estimativa: {total_bytes:,} bytes")
                    active_flows.clear()
                else:
                    print("[*] Aguardando tráfego IP ativo...")
    except KeyboardInterrupt:
        print("\n[*] A encerrar...")