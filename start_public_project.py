#!/usr/bin/env python3
"""
Финальный запуск Upwork Proposal Generator с публичным доступом
"""

import subprocess
import time
import threading
import signal
import sys
import os

def print_banner():
    print("=" * 60)
    print("🚀 UPWORK PROPOSAL GENERATOR - ПУБЛИЧНАЯ ВЕРСИЯ")
    print("=" * 60)
    print("AI-помощник для создания выигрышных предложений на Upwork")
    print("🌐 Доступен везде | 📱 Все устройства | 🔒 Защищен")
    print("=" * 60)

def start_backend():
    """Запускает backend сервер"""
    print("🔧 Запуск защищенного backend сервера...")
    
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
            print("✅ Backend сервер запущен с защитой!")
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
            print("✅ Frontend сервер запущен!")
            return process
        else:
            print("❌ Ошибка запуска frontend сервера")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запуска frontend: {e}")
        return None

def start_public_proxy():
    """Запускает публичный прокси сервер"""
    print("🌐 Запуск публичного прокси сервера...")
    
    os.chdir(os.path.dirname(__file__))
    
    try:
        # Запускаем на порту 8080 для публичного доступа
        process = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8080", "--bind", "0.0.0.0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Ждем немного для запуска
        time.sleep(2)
        
        if process.poll() is None:
            print("✅ Публичный прокси сервер запущен!")
            return process
        else:
            print("❌ Ошибка запуска публичного прокси")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запуска публичного прокси: {e}")
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
    
    # Запускаем публичный прокси
    proxy_process = start_public_proxy()
    if not proxy_process:
        print("❌ Не удалось запустить публичный прокси")
        return
    
    print("\n" + "=" * 60)
    print("🎉 ПРОЕКТ УСПЕШНО ЗАПУЩЕН С ПУБЛИЧНЫМ ДОСТУПОМ!")
    print("=" * 60)
    print("🌐 Основной URL: http://192.168.0.124:3000")
    print("🌍 Публичный URL: http://192.168.0.124:8080")
    print("📱 Доступен на всех устройствах в сети")
    print("🔒 Защищенное соединение активировано")
    print("=" * 60)
    print("📚 API документация: http://192.168.0.124:8000/docs")
    print("🔧 Backend API: http://192.168.0.124:8000/api/")
    print("=" * 60)
    print("💡 Для доступа из интернета настройте проброс портов:")
    print("   - Порт 3000 (frontend)")
    print("   - Порт 8000 (backend)")
    print("   - Порт 8080 (публичный доступ)")
    print("=" * 60)
    print("💡 Для остановки нажмите Ctrl+C")
    print("=" * 60)
    
    # Обработчик сигналов для корректного завершения
    def signal_handler(sig, frame):
        print("\n🛑 Остановка всех серверов...")
        for process in [backend_process, frontend_process, proxy_process]:
            if process and process.poll() is None:
                process.terminate()
                process.wait()
        print("✅ Все серверы остановлены")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Ждем завершения процессов
    try:
        while True:
            time.sleep(1)
            # Проверяем, что все процессы еще работают
            if (backend_process.poll() is not None or 
                frontend_process.poll() is not None or 
                proxy_process.poll() is not None):
                print("❌ Один из серверов остановился")
                break
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main() 