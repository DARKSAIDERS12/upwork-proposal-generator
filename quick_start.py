#!/usr/bin/env python3
"""
Быстрый запуск Upwork Proposal Generator
"""

import subprocess
import time
import os
import sys

def print_banner():
    print("=" * 60)
    print("🚀 UPWORK PROPOSAL GENERATOR - БЫСТРЫЙ ЗАПУСК")
    print("=" * 60)
    print("AI-помощник для создания выигрышных предложений на Upwork")
    print("=" * 60)

def start_servers():
    """Запускает оба сервера"""
    print("🔧 Запуск серверов...")
    
    # Останавливаем старые процессы
    os.system("pkill -f 'python.*run.py' 2>/dev/null")
    os.system("pkill -f 'python.*server.py' 2>/dev/null")
    
    # Запускаем backend
    print("📡 Запуск backend сервера...")
    backend_cmd = "cd backend && source venv/bin/activate && nohup python run.py > backend.log 2>&1 &"
    subprocess.run(backend_cmd, shell=True)
    
    # Запускаем frontend
    print("🎨 Запуск frontend сервера...")
    frontend_cmd = "cd frontend && nohup python3 server.py > frontend.log 2>&1 &"
    subprocess.run(frontend_cmd, shell=True)
    
    # Ждем запуска
    print("⏳ Ожидание запуска серверов...")
    time.sleep(8)
    
    print("✅ Серверы запущены!")

def check_servers():
    """Проверяет работу серверов"""
    import requests
    
    print("\n🔍 Проверка серверов...")
    
    try:
        # Проверка backend
        response = requests.get("http://192.168.0.124:8000/health", timeout=3)
        if response.status_code == 200:
            print("✅ Backend: http://192.168.0.124:8000")
        else:
            print("❌ Backend не отвечает")
    except:
        print("❌ Backend не отвечает")
    
    try:
        # Проверка frontend
        response = requests.get("http://192.168.0.124:3000", timeout=3)
        if response.status_code == 200:
            print("✅ Frontend: http://192.168.0.124:3000")
        else:
            print("❌ Frontend не отвечает")
    except:
        print("❌ Frontend не отвечает")

def main():
    print_banner()
    
    # Запускаем серверы
    start_servers()
    
    # Проверяем работу
    check_servers()
    
    print("\n" + "=" * 60)
    print("🎉 ПРОЕКТ ГОТОВ К ИСПОЛЬЗОВАНИЮ!")
    print("=" * 60)
    print("📱 Frontend: http://192.168.0.124:3000")
    print("🔧 Backend API: http://192.168.0.124:8000")
    print("📚 API документация: http://192.168.0.124:8000/docs")
    print("=" * 60)
    print("💡 Для остановки: ./stop_servers.py")
    print("=" * 60)

if __name__ == "__main__":
    main() 