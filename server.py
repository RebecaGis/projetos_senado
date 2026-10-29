#!/usr/bin/env python3
"""
Servidor local do App de Letramento Político (e-Cidadania)
Inicia um servidor web local com suporte a API e acesso via rede Wi-Fi / Celular.
"""

import http.server
import socketserver
import os
import sys
import json
import socket

# Configurar stdout para UTF-8 sem erro no Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from update_ecidadania import parse_ecidadania

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class AppHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_GET(self):
        if self.path == '/api/proposicoes':
            json_path = os.path.join(BASE_DIR, 'proposicoes.json')
            if not os.path.exists(json_path):
                parse_ecidadania()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            with open(json_path, 'rb') as f:
                self.wfile.write(f.read())
            return
            
        elif self.path == '/api/atualizar':
            try:
                data = parse_ecidadania()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                res = json.dumps({'status': 'ok', 'count': len(data), 'message': 'Consultas atualizadas com sucesso direto do Senado!'}, ensure_ascii=False)
                self.wfile.write(res.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                res = json.dumps({'status': 'error', 'message': str(e)}, ensure_ascii=False)
                self.wfile.write(res.encode('utf-8'))
            return
            
        return super().do_GET()

def run_server():
    os.chdir(BASE_DIR)
    local_ip = get_local_ip()
    socketserver.TCPServer.allow_reuse_address = True
    
    port = PORT
    httpd = None
    for p in [8080, 8081, 8082, 3000, 5000]:
        try:
            httpd = socketserver.TCPServer(("", p), AppHandler)
            port = p
            break
        except OSError:
            continue
            
    if not httpd:
        print("Erro: Nenhuma porta disponível encontrada.")
        return
        
    with httpd:
        print("=" * 60)
        print("  APP DE LETRAMENTO POLITICO - SENADO E-CIDADANIA")
        print("=" * 60)
        print("Servidor ativo e atualizado:")
        print(f" -> Computador: http://localhost:{port}")
        print(f" -> Celular (mesma Wi-Fi): http://{local_ip}:{port}")
        print("=" * 60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")

if __name__ == '__main__':
    run_server()
