#!/usr/bin/env python3
"""
Комплексный запуск Upwork Proposal Generator с HTTPS
"""

import subprocess
import time
import threading
import signal
import sys
import os

def print_banner():
    print("=" * 60)
    print("🚀 UPWORK PROPOSAL GENERATOR - HTTPS ВЕРСИЯ")
    print("=" * 60)
    print("AI-помощник для создания выигрышных предложений на Upwork")
    print("🔒 Безопасное соединение | 📱 Доступен везде")
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

def start_https_proxy():
    """Запускает HTTPS прокси сервер"""
    print("🔒 Запуск HTTPS прокси сервера...")
    
    os.chdir(os.path.dirname(__file__))
    
    try:
        process = subprocess.Popen(
            [sys.executable, "https_proxy.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Ждем немного для запуска
        time.sleep(2)
        
        if process.poll() is None:
            print("✅ HTTPS прокси сервер запущен!")
            return process
        else:
            print("❌ Ошибка запуска HTTPS прокси")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запуска HTTPS прокси: {e}")
        return None

def check_ssl_certificates():
    """Проверяет наличие SSL сертификатов"""
    cert_file = os.path.join(os.path.dirname(__file__), "cert.pem")
    key_file = os.path.join(os.path.dirname(__file__), "key.pem")
    
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("❌ SSL сертификаты не найдены!")
        print("🔧 Создаю SSL сертификаты...")
        
        os.chdir(os.path.dirname(__file__))
        cmd = "openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/C=RU/ST=Moscow/L=Moscow/O=UpworkProposalGenerator/CN=192.168.0.124'"
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            print("✅ SSL сертификаты созданы!")
        except subprocess.CalledProcessError:
            print("❌ Ошибка создания SSL сертификатов")
            return False
    
    return True

def main():
    print_banner()
    
    # Проверяем SSL сертификаты
    if not check_ssl_certificates():
        return
    
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
    
    # Запускаем HTTPS прокси
    https_process = start_https_proxy()
    if not https_process:
        print("❌ Не удалось запустить HTTPS прокси")
        return
    
    print("\n" + "=" * 60)
    print("🎉 ПРОЕКТ УСПЕШНО ЗАПУЩЕН С HTTPS!")
    print("=" * 60)
    print("🌐 Основной URL: https://192.168.0.124")
    print("📱 Доступен на всех устройствах в сети")
    print("🔒 Безопасное соединение активировано")
    print("=" * 60)
    print("📚 API документация: https://192.168.0.124/api/docs")
    print("🔧 Backend API: https://192.168.0.124/api/")
    print("=" * 60)
    print("💡 Для остановки нажмите Ctrl+C")
    print("=" * 60)
    
    # Обработчик сигналов для корректного завершения
    def signal_handler(sig, frame):
        print("\n🛑 Остановка всех серверов...")
        for process in [backend_process, frontend_process, https_process]:
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
                https_process.poll() is not None):
                print("❌ Один из серверов остановился")
                break
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main() 