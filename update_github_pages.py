#!/usr/bin/env python3
"""
🔄 ОБНОВЛЕНИЕ GITHUB PAGES
============================================================
Скрипт для принудительного обновления GitHub Pages
"""

import subprocess
import time
import requests
import os

def run_command(command):
    """Выполнение команды"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_github_pages():
    """Проверка текущего состояния GitHub Pages"""
    print("🔍 Проверка GitHub Pages...")
    
    url = "https://darksaiders12.github.io/upwork-proposal-generator/"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            content = response.text
            if "subscription" in content.lower() or "premium" in content.lower():
                print("✅ GitHub Pages обновлен - система подписок найдена!")
                return True
            else:
                print("❌ GitHub Pages не обновлен - система подписок не найдена")
                return False
        else:
            print(f"❌ Ошибка доступа к GitHub Pages: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка при проверке GitHub Pages: {e}")
        return False

def force_update():
    """Принудительное обновление GitHub Pages"""
    print("🔄 Принудительное обновление GitHub Pages...")
    
    # Проверяем текущую ветку
    success, stdout, stderr = run_command("git branch --show-current")
    if not success:
        print(f"❌ Ошибка определения ветки: {stderr}")
        return False
    
    current_branch = stdout.strip()
    print(f"📋 Текущая ветка: {current_branch}")
    
    # Создаем файл для принудительного обновления
    timestamp = int(time.time())
    update_file = f"update_{timestamp}.txt"
    
    with open(update_file, "w") as f:
        f.write(f"GitHub Pages Update: {timestamp}\n")
        f.write("This file forces GitHub Pages to rebuild\n")
    
    # Коммитим и пушим изменения
    commands = [
        f"git add {update_file}",
        f"git commit -m 'Force GitHub Pages update {timestamp}'",
        "git push origin main"
    ]
    
    for cmd in commands:
        success, stdout, stderr = run_command(cmd)
        if not success:
            print(f"❌ Ошибка выполнения команды '{cmd}': {stderr}")
            return False
        print(f"✅ Выполнено: {cmd}")
    
    # Удаляем временный файл
    os.remove(update_file)
    run_command(f"git add {update_file}")
    run_command(f"git commit -m 'Remove temporary update file'")
    run_command("git push origin main")
    
    return True

def wait_for_update(max_wait=300):
    """Ожидание обновления GitHub Pages"""
    print(f"⏳ Ожидание обновления GitHub Pages (максимум {max_wait} секунд)...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        if check_github_pages():
            return True
        
        print("⏳ Ожидание... (30 секунд)")
        time.sleep(30)
    
    print("⏰ Время ожидания истекло")
    return False

def main():
    """Основная функция"""
    print("=" * 60)
    print("🔄 ОБНОВЛЕНИЕ GITHUB PAGES")
    print("=" * 60)
    
    # Проверяем текущее состояние
    if check_github_pages():
        print("✅ GitHub Pages уже обновлен!")
        return
    
    # Принудительно обновляем
    if force_update():
        print("✅ Изменения отправлены в GitHub")
        
        # Ждем обновления
        if wait_for_update():
            print("🎉 GitHub Pages успешно обновлен!")
        else:
            print("⚠️ GitHub Pages не обновился в ожидаемое время")
            print("💡 Попробуйте проверить вручную через несколько минут")
    else:
        print("❌ Не удалось обновить GitHub Pages")

if __name__ == "__main__":
    main() 