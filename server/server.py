import subprocess

print("[*] Este script depende do MediaMTX -> instale antes")

def start_lightweight_stream():
    # Comando FFmpeg ultra-leve: lê o arquivo, faz loop infinito, e empurra para o MediaMTX
    # O '-c copy' garante ZERO uso de CPU com encoding (copia o fluxo original do MP4)
    cmd = [
        "ffmpeg",
        "-stream_loop", "-1",          # Mantém o vídeo em looping infinito
        "-re",                         # Sincroniza com o framerate original do vídeo (fps real)
        "-i", "video.mp4",             # Arquivo de vídeo de origem
        "-c", "copy",                  # Copia os codecs originais (sem re-encode de CPU)
        "-f", "rtsp",                  # Formato de saída
        "rtsp://localhost:8554/stream" # Envia para o MediaMTX rodando no host1
    ]
    
    print("[*] Iniciando streaming leve para o MediaMTX...")
    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return process

if __name__ == "__main__":
    proc = start_lightweight_stream()
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()