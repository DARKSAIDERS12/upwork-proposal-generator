#!/usr/bin/env python3
"""
Автоматический запуск Upwork Proposal Generator с пробросом портов
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
    print("🚀 UPWORK PROPOSAL GENERATOR - АВТОМАТИЧЕСКИЙ ПРОБРОС")
    print("=" * 60)
    print("AI-помощник для создания выигрышных предложений на Upwork")
    print("🌐 Доступен из интернета | 📱 Все устройства | 🔒 Защищен")
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

def start_ngrok_tunnel():
    """Запускает ngrok туннель для frontend"""
    print("🌐 Запуск ngrok туннеля для frontend...")
    
    os.chdir(os.path.dirname(__file__))
    
    try:
        # Запускаем ngrok для frontend (порт 3000)
        process = subprocess.Popen(
            ["./ngrok", "http", "3000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Ждем немного для запуска
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Ngrok туннель запущен!")
            return process
        else:
            print("❌ Ошибка запуска ngrok туннеля")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запуска ngrok: {e}")
        return None

def get_ngrok_url():
    """Получает публичный URL от ngrok"""
    try:
        # Получаем информацию о туннелях
        response = requests.get("http://localhost:4040/api/tunnels")
        if response.status_code == 200:
            tunnels = response.json()["tunnels"]
            for tunnel in tunnels:
                if tunnel["proto"] == "https":
                    return tunnel["public_url"]
    except:
        pass
    return None

def start_ngrok_api_tunnel():
    """Запускает ngrok туннель для API"""
    print("🔧 Запуск ngrok туннеля для API...")
    
    os.chdir(os.path.dirname(__file__))
    
    try:
        # Запускаем ngrok для API (порт 8000)
        process = subprocess.Popen(
            ["./ngrok", "http", "8000", "--log=stdout"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Ждем немного для запуска
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Ngrok API туннель запущен!")
            return process
        else:
            print("❌ Ошибка запуска ngrok API туннеля")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запуска ngrok API: {e}")
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
    
    # Запускаем ngrok туннель для frontend
    ngrok_process = start_ngrok_tunnel()
    if not ngrok_process:
        print("❌ Не удалось запустить ngrok туннель")
        return
    
    # Ждем немного и получаем URL
    time.sleep(10)
    public_url = get_ngrok_url()
    
    print("\n" + "=" * 60)
    print("🎉 ПРОЕКТ УСПЕШНО ЗАПУЩЕН С АВТОМАТИЧЕСКИМ ПРОБРОСОМ!")
    print("=" * 60)
    
    if public_url:
        print(f"🌐 ПУБЛИЧНЫЙ URL: {public_url}")
        print("📱 Доступен из интернета на всех устройствах!")
    else:
        print("🌐 Публичный URL будет доступен через несколько секунд...")
        print("💡 Проверьте: http://localhost:4040")
    
    print("=" * 60)
    print("🔗 Локальные URL:")
    print("   Frontend: http://192.168.0.124:3000")
    print("   Backend: http://192.168.0.124:8000")
    print("   API Docs: http://192.168.0.124:8000/docs")
    print("=" * 60)
    print("🔒 Безопасность: Rate limiting, Security headers, CORS")
    print("=" * 60)
    print("💡 Для остановки нажмите Ctrl+C")
    print("=" * 60)
    
    # Обработчик сигналов для корректного завершения
    def signal_handler(sig, frame):
        print("\n🛑 Остановка всех серверов...")
        for process in [backend_process, frontend_process, ngrok_process]:
            if process and process.poll() is None:
                process.terminate()
                process.wait()
        print("✅ Все серверы остановлены")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Периодически показываем публичный URL
    def show_url():
        while True:
            time.sleep(30)
            url = get_ngrok_url()
            if url:
                print(f"\n🌐 ПУБЛИЧНЫЙ URL: {url}")
                print("📱 Доступен из интернета!")
    
    # Запускаем поток для показа URL
    url_thread = threading.Thread(target=show_url, daemon=True)
    url_thread.start()
    
    # Ждем завершения процессов
    try:
        while True:
            time.sleep(1)
            # Проверяем, что все процессы еще работают
            if (backend_process.poll() is not None or 
                frontend_process.poll() is not None or 
                ngrok_process.poll() is not None):
                print("❌ Один из серверов остановился")
                break
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main() 