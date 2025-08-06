#!/usr/bin/env python3
"""
Настройка HTTPS и публичного доступа для Upwork Proposal Generator
"""

import subprocess
import time
import threading
import signal
import sys
import os
import json
import requests

def print_banner():
    print("=" * 60)
    print("🌐 НАСТРОЙКА ПУБЛИЧНОГО ДОСТУПА И HTTPS")
    print("=" * 60)
    print("AI-помощник для создания выигрышных предложений на Upwork")
    print("🔒 HTTPS | 📱 Все устройства | 🌍 Доступен везде")
    print("=" * 60)

def check_ngrok():
    """Проверяет наличие ngrok"""
    if os.path.exists("./ngrok"):
        print("✅ Ngrok найден")
        return True
    else:
        print("❌ Ngrok не найден")
        return False

def start_servers():
    """Запускает серверы"""
    print("🔧 Запуск серверов...")
    
    # Останавливаем старые процессы
    os.system("pkill -f 'python.*run.py' 2>/dev/null")
    os.system("pkill -f 'python.*server.py' 2>/dev/null")
    os.system("pkill -f ngrok 2>/dev/null")
    
    # Запускаем backend
    print("📡 Запуск backend сервера...")
    backend_cmd = "cd backend && . venv/bin/activate && nohup python run.py > backend.log 2>&1 &"
    subprocess.run(backend_cmd, shell=True)
    
    # Запускаем frontend
    print("🎨 Запуск frontend сервера...")
    frontend_cmd = "cd frontend && nohup python3 server.py > frontend.log 2>&1 &"
    subprocess.run(frontend_cmd, shell=True)
    
    # Ждем запуска
    print("⏳ Ожидание запуска серверов...")
    time.sleep(8)
    
    print("✅ Серверы запущены!")

def start_ngrok_tunnels():
    """Запускает ngrok туннели"""
    print("🌐 Запуск ngrok туннелей...")
    
    # Запускаем туннель для backend
    print("📡 Создание туннеля для backend (порт 8000)...")
    backend_tunnel = subprocess.Popen(
        ["./ngrok", "http", "8000", "--log=stdout"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Запускаем туннель для frontend
    print("🎨 Создание туннеля для frontend (порт 3000)...")
    frontend_tunnel = subprocess.Popen(
        ["./ngrok", "http", "3000", "--log=stdout"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Ждем запуска туннелей
    print("⏳ Ожидание запуска туннелей...")
    time.sleep(5)
    
    return backend_tunnel, frontend_tunnel

def get_ngrok_urls():
    """Получает публичные URL от ngrok"""
    print("🔍 Получение публичных URL...")
    
    try:
        # Получаем URL для backend
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            tunnels = response.json()["tunnels"]
            
            backend_url = None
            frontend_url = None
            
            for tunnel in tunnels:
                if tunnel["config"]["addr"] == "http://localhost:8000":
                    backend_url = tunnel["public_url"]
                elif tunnel["config"]["addr"] == "http://localhost:3000":
                    frontend_url = tunnel["public_url"]
            
            return backend_url, frontend_url
    except:
        pass
    
    return None, None

def update_frontend_config(backend_url):
    """Обновляет конфигурацию frontend для работы с публичным backend"""
    if not backend_url:
        return
    
    print("🔧 Обновление конфигурации frontend...")
    
    frontend_js = "frontend/app.js"
    if os.path.exists(frontend_js):
        with open(frontend_js, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Заменяем локальный URL на публичный
        content = content.replace("http://192.168.0.124:8000", backend_url)
        content = content.replace("http://localhost:8000", backend_url)
        
        with open(frontend_js, "w", encoding="utf-8") as f:
            f.write(content)
        
        print("✅ Конфигурация frontend обновлена")

def check_servers():
    """Проверяет работу серверов"""
    print("\n🔍 Проверка серверов...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=3)
        if response.status_code == 200:
            print("✅ Backend: http://localhost:8000")
        else:
            print("❌ Backend не отвечает")
    except:
        print("❌ Backend не отвечает")
    
    try:
        response = requests.get("http://localhost:3000", timeout=3)
        if response.status_code == 200:
            print("✅ Frontend: http://localhost:3000")
        else:
            print("❌ Frontend не отвечает")
    except:
        print("❌ Frontend не отвечает")

def main():
    print_banner()
    
    # Проверяем ngrok
    if not check_ngrok():
        print("❌ Не удалось найти ngrok. Установите ngrok для публичного доступа.")
        return
    
    # Запускаем серверы
    start_servers()
    
    # Проверяем серверы
    check_servers()
    
    # Запускаем туннели
    backend_tunnel, frontend_tunnel = start_ngrok_tunnels()
    
    # Получаем публичные URL
    backend_url, frontend_url = get_ngrok_urls()
    
    # Обновляем конфигурацию frontend
    update_frontend_config(backend_url)
    
    # Показываем результаты
    print("\n" + "=" * 60)
    print("🎉 ПУБЛИЧНЫЙ ДОСТУП НАСТРОЕН!")
    print("=" * 60)
    
    if frontend_url:
        print(f"🌐 Публичный сайт: {frontend_url}")
        print(f"🔒 HTTPS доступ: {frontend_url.replace('http://', 'https://')}")
    else:
        print("⚠️  Публичный URL не получен")
    
    if backend_url:
        print(f"🔧 Публичный API: {backend_url}")
        print(f"📚 API документация: {backend_url}/docs")
    else:
        print("⚠️  Публичный API URL не получен")
    
    print("\n📱 Теперь сайт доступен:")
    print("   - На всех устройствах")
    print("   - Из любой точки мира")
    print("   - По HTTPS (защищенное соединение)")
    print("   - Через любой браузер")
    
    print("\n💡 Для остановки: Ctrl+C")
    print("=" * 60)
    
    try:
        # Ждем завершения
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Остановка серверов...")
        os.system("pkill -f 'python.*run.py' 2>/dev/null")
        os.system("pkill -f 'python.*server.py' 2>/dev/null")
        os.system("pkill -f ngrok 2>/dev/null")
        print("✅ Серверы остановлены!")

if __name__ == "__main__":
    main() 