#!/usr/bin/env python3
"""
Получение публичного URL для Upwork Proposal Generator
"""

import subprocess
import time
import requests
import json

def start_ngrok():
    """Запускает ngrok туннель"""
    print("🌐 Запуск ngrok туннеля...")
    
    try:
        # Запускаем ngrok для frontend
        process = subprocess.Popen(
            ["./ngrok", "http", "3000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Ждем запуска
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Ngrok туннель запущен!")
            return process
        else:
            print("❌ Ошибка запуска ngrok")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def get_public_url():
    """Получает публичный URL от ngrok"""
    try:
        # Получаем информацию о туннелях
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            tunnels = response.json()["tunnels"]
            for tunnel in tunnels:
                if tunnel["proto"] == "https":
                    return tunnel["public_url"]
    except Exception as e:
        print(f"Ошибка получения URL: {e}")
    return None

def main():
    print("=" * 60)
    print("🌐 ПОЛУЧЕНИЕ ПУБЛИЧНОГО URL")
    print("=" * 60)
    
    # Запускаем ngrok
    ngrok_process = start_ngrok()
    if not ngrok_process:
        print("❌ Не удалось запустить ngrok")
        return
    
    print("⏳ Ожидание создания туннеля...")
    
    # Пытаемся получить URL несколько раз
    for i in range(10):
        time.sleep(3)
        url = get_public_url()
        if url:
            print("\n" + "=" * 60)
            print("🎉 ПУБЛИЧНЫЙ URL ПОЛУЧЕН!")
            print("=" * 60)
            print(f"🌐 URL: {url}")
            print("📱 Доступен из интернета на всех устройствах!")
            print("=" * 60)
            print("💡 Скопируйте этот URL и отправьте друзьям!")
            print("=" * 60)
            break
        else:
            print(f"⏳ Попытка {i+1}/10...")
    
    if not url:
        print("❌ Не удалось получить публичный URL")
        print("💡 Проверьте: http://localhost:4040")
    
    # Ждем завершения
    try:
        ngrok_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Остановка ngrok...")
        ngrok_process.terminate()
        print("✅ Ngrok остановлен")

if __name__ == "__main__":
    main() 