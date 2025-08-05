#!/usr/bin/env python3
"""
HTTPS прокси сервер для Upwork Proposal Generator
Обеспечивает безопасный доступ к сайту через HTTPS
"""

import ssl
import socket
import threading
import http.server
import urllib.request
import urllib.parse
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class HTTPSProxyHandler(BaseHTTPRequestHandler):
    """Обработчик HTTPS прокси запросов"""
    
    def do_GET(self):
        """Обработка GET запросов"""
        try:
            # Определяем целевой сервер
            if self.path.startswith('/api/'):
                # API запросы идут на backend
                target_url = f"http://localhost:8000{self.path}"
            else:
                # Остальные запросы идут на frontend
                target_url = f"http://localhost:3000{self.path}"
            
            # Создаем запрос к целевому серверу
            req = urllib.request.Request(target_url)
            
            # Копируем заголовки
            for header, value in self.headers.items():
                if header.lower() not in ['host', 'connection']:
                    req.add_header(header, value)
            
            # Выполняем запрос
            with urllib.request.urlopen(req) as response:
                # Отправляем статус код
                self.send_response(response.status)
                
                # Отправляем заголовки
                for header, value in response.getheaders():
                    if header.lower() not in ['transfer-encoding']:
                        self.send_header(header, value)
                
                # Добавляем CORS заголовки
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                
                self.end_headers()
                
                # Отправляем содержимое
                self.wfile.write(response.read())
                
        except Exception as e:
            print(f"Ошибка обработки запроса: {e}")
            self.send_error(500, f"Internal Server Error: {e}")
    
    def do_POST(self):
        """Обработка POST запросов"""
        try:
            # Определяем целевой сервер
            if self.path.startswith('/api/'):
                target_url = f"http://localhost:8000{self.path}"
            else:
                target_url = f"http://localhost:3000{self.path}"
            
            # Читаем тело запроса
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # Создаем запрос
            req = urllib.request.Request(target_url, data=post_data, method='POST')
            
            # Копируем заголовки
            for header, value in self.headers.items():
                if header.lower() not in ['host', 'connection', 'content-length']:
                    req.add_header(header, value)
            
            # Выполняем запрос
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                
                # Отправляем заголовки
                for header, value in response.getheaders():
                    if header.lower() not in ['transfer-encoding']:
                        self.send_header(header, value)
                
                # Добавляем CORS заголовки
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                
                self.end_headers()
                
                # Отправляем содержимое
                self.wfile.write(response.read())
                
        except Exception as e:
            print(f"Ошибка обработки POST запроса: {e}")
            self.send_error(500, f"Internal Server Error: {e}")
    
    def do_OPTIONS(self):
        """Обработка OPTIONS запросов для CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Логирование запросов"""
        print(f"📡 HTTPS: {format % args}")

def start_https_server():
    """Запуск HTTPS сервера"""
    # Создаем SSL контекст
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    
    # Создаем HTTP сервер
    server = HTTPServer(('0.0.0.0', 443), HTTPSProxyHandler)
    
    # Оборачиваем в SSL
    server.socket = context.wrap_socket(server.socket, server_side=True)
    
    print("🔒 HTTPS прокси сервер запущен!")
    print("🌐 URL: https://192.168.0.124")
    print("📱 Доступен на всех устройствах в сети")
    print("🔐 Безопасное соединение активировано")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Остановка HTTPS сервера...")
        server.shutdown()
        print("✅ HTTPS сервер остановлен")

if __name__ == "__main__":
    print("=" * 60)
    print("🔒 HTTPS ПРОКСИ СЕРВЕР")
    print("=" * 60)
    print("AI-помощник для создания выигрышных предложений на Upwork")
    print("=" * 60)
    
    # Проверяем наличие сертификатов
    if not os.path.exists('cert.pem') or not os.path.exists('key.pem'):
        print("❌ SSL сертификаты не найдены!")
        print("💡 Создайте их командой:")
        print("openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes")
        exit(1)
    
    start_https_server() 