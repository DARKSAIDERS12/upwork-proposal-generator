#!/usr/bin/env python3
"""
Проверка деплоя русской премиум системы на GitHub Pages
"""

import requests
import time
from datetime import datetime

def check_deployment_status():
    """Проверяет статус деплоя на GitHub Pages"""
    print("🔍 Проверка деплоя русской премиум системы на GitHub Pages...")
    print("=" * 60)
    
    base_url = "https://darksaiders12.github.io/upwork-proposal-generator"
    
    # Проверяем основные файлы
    files_to_check = [
        "",  # Главная страница
        "/subscription_manager.html",  # Менеджер подписок
        "/app.js",  # Обновленный JavaScript
        "/styles.css"  # Стили
    ]
    
    print(f"🌐 Проверяем сайт: {base_url}")
    print("=" * 60)
    
    all_ok = True
    
    for file_path in files_to_check:
        url = base_url + file_path
        file_name = "index.html" if file_path == "" else file_path.lstrip("/")
        
        try:
            print(f"📄 Проверяем {file_name}...", end=" ")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Дополнительные проверки для специфических файлов
                if file_path == "":
                    if "🇷🇺 Ваша подписка" in response.text:
                        print("✅ Русская система найдена!")
                    else:
                        print("⚠️ Загружен, но русская система не найдена")
                        all_ok = False
                elif file_path == "/subscription_manager.html":
                    if "Yandex GPT" in response.text:
                        print("✅ Менеджер подписок работает!")
                    else:
                        print("⚠️ Загружен, но содержимое неполное")
                        all_ok = False
                elif file_path == "/app.js":
                    if "РУССКАЯ ПРЕМИУМ AI СИСТЕМА" in response.text:
                        print("✅ Премиум логика найдена!")
                    else:
                        print("⚠️ Загружен, но премиум код не найден")
                        all_ok = False
                else:
                    print("✅ Загружен успешно")
            else:
                print(f"❌ Ошибка {response.status_code}")
                all_ok = False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка соединения: {e}")
            all_ok = False
        
        time.sleep(1)  # Пауза между запросами
    
    print("=" * 60)
    
    if all_ok:
        print("🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
        print("✅ Русская премиум система полностью развернута")
        print(f"🌐 Сайт доступен: {base_url}")
        print(f"💎 Менеджер подписок: {base_url}/subscription_manager.html")
    else:
        print("⚠️ Некоторые проверки не прошли")
        print("💡 GitHub Pages может потребовать несколько минут для обновления")
        print("🔄 Попробуйте повторить проверку через 2-3 минуты")
    
    return all_ok

def check_specific_features():
    """Проверяет специфические функции русской системы"""
    print("\n🔍 Проверка специфических функций...")
    print("=" * 40)
    
    base_url = "https://darksaiders12.github.io/upwork-proposal-generator"
    
    try:
        # Проверяем главную страницу на наличие русских элементов
        response = requests.get(base_url, timeout=10)
        content = response.text
        
        features = [
            ("🇷🇺 Эмодзи флага", "🇷🇺" in content),
            ("Yandex GPT упоминание", "Yandex GPT" in content),
            ("Русские тарифы", "RUB" in content or "рублей" in content),
            ("Премиум кнопка", "Премиум" in content or "Premium" in content),
            ("Подписка интерфейс", "подписка" in content.lower()),
            ("AI провайдер", "AI:" in content or "провайдер" in content)
        ]
        
        for feature_name, is_present in features:
            status = "✅" if is_present else "❌"
            print(f"{status} {feature_name}")
        
        # Проверяем менеджер подписок
        subscription_url = f"{base_url}/subscription_manager.html"
        sub_response = requests.get(subscription_url, timeout=10)
        
        if sub_response.status_code == 200:
            sub_content = sub_response.text
            print(f"✅ Менеджер подписок доступен")
            
            if "1,500" in sub_content and "3,000" in sub_content:
                print(f"✅ Русские цены найдены")
            else:
                print(f"⚠️ Русские цены не найдены")
        else:
            print(f"❌ Менеджер подписок недоступен")
        
    except Exception as e:
        print(f"❌ Ошибка проверки: {e}")

def main():
    print("🚀 ПРОВЕРКА ДЕПЛОЯ РУССКОЙ ПРЕМИУМ СИСТЕМЫ")
    print("=" * 60)
    print(f"⏰ Время проверки: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print()
    
    # Основная проверка
    deployment_ok = check_deployment_status()
    
    # Проверка специфических функций
    check_specific_features()
    
    print("\n" + "=" * 60)
    if deployment_ok:
        print("🎯 ДЕПЛОЙ ЗАВЕРШЕН УСПЕШНО!")
        print("🌐 Сайт: https://darksaiders12.github.io/upwork-proposal-generator/")
        print("💎 Подписки: https://darksaiders12.github.io/upwork-proposal-generator/subscription_manager.html")
        print("\n📋 Что дальше:")
        print("1. Получите Yandex GPT API ключ на cloud.yandex.ru")
        print("2. Протестируйте все функции на публичном сайте")
        print("3. Настройте систему платежей")
        print("4. Запустите маркетинг!")
    else:
        print("⚠️ ДЕПЛОЙ ТРЕБУЕТ ВНИМАНИЯ")
        print("💡 GitHub Pages может потребовать время для обновления")
        print("🔄 Повторите проверку через несколько минут")

if __name__ == "__main__":
    main()