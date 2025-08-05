#!/usr/bin/env python3
"""
Простой веб-сервер для frontend
"""

import http.server
import socketserver
import os
import sys

# Настройки сервера
PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Добавляем CORS заголовки
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Обработка preflight запросов
        self.send_response(200)
        self.end_headers()

def main():
    print(f"🚀 Запуск frontend сервера на http://192.168.0.124:{PORT}")
    print(f"📁 Директория: {DIRECTORY}")
    print("🌐 Откройте браузер и перейдите по адресу: http://192.168.0.124:3000")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"✅ Сервер запущен на порту {PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Порт {PORT} уже занят. Попробуйте другой порт.")
        else:
            print(f"❌ Ошибка запуска сервера: {e}")

if __name__ == "__main__":
    main() 