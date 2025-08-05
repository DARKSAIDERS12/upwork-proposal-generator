#!/usr/bin/env python3
"""
Скрипт для запуска серверов с правильными IP адресами
"""

import subprocess
import time
import threading
import signal
import sys
import os

def print_banner():
    print("=" * 60)
    print("🚀 UPWORK PROPOSAL GENERATOR")
    print("=" * 60)
    print("AI-помощник для создания выигрышных предложений на Upwork")
    print("=" * 60)

def start_backend():
    """Запускает backend сервер"""
    print("🔧 Запуск backend сервера...")
    
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    os.chdir(backend_dir)
    
    # Активируем виртуальное окружение и запускаем сервер
    cmd = f"source venv/bin/activate && python run.py"
    
    try:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Ждем немного для запуска
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Backend сервер запущен на http://192.168.0.124:8000")
            return process
        else:
            print("❌ Ошибка запуска backend сервера")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запуска backend: {e}")
        return None

def start_frontend():
    """Запускает frontend сервер"""
    print("🎨 Запуск frontend сервера...")
    
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    os.chdir(frontend_dir)
    
    try:
        process = subprocess.Popen(
            [sys.executable, "server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Ждем немного для запуска
        time.sleep(2)
        
        if process.poll() is None:
            print("✅ Frontend сервер запущен на http://192.168.0.124:3000")
            return process
        else:
            print("❌ Ошибка запуска frontend сервера")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запуска frontend: {e}")
        return None

def main():
    print_banner()
    
    # Запускаем backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Не удалось запустить backend сервер")
        return
    
    # Запускаем frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Не удалось запустить frontend сервер")
        return
    
    print("\n" + "=" * 60)
    print("🎉 ПРОЕКТ УСПЕШНО ЗАПУЩЕН!")
    print("=" * 60)
    print("📱 Frontend: http://192.168.0.124:3000")
    print("🔧 Backend API: http://192.168.0.124:8000")
    print("📚 API документация: http://192.168.0.124:8000/docs")
    print("=" * 60)
    print("💡 Для остановки нажмите Ctrl+C")
    print("=" * 60)
    
    try:
        # Ждем завершения процессов
        while True:
            time.sleep(1)
            
            # Проверяем, что процессы еще работают
            if backend_process and backend_process.poll() is not None:
                print("❌ Backend сервер остановился")
                break
                
            if frontend_process and frontend_process.poll() is not None:
                print("❌ Frontend сервер остановился")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Остановка серверов...")
        
        # Останавливаем процессы
        if backend_process:
            backend_process.terminate()
            print("✅ Backend сервер остановлен")
            
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend сервер остановлен")
        
        print("👋 Проект остановлен")

if __name__ == "__main__":
    main() 