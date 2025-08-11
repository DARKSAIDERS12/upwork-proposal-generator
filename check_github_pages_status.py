#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для проверки статуса GitHub Pages
Проверяет доступность всех созданных страниц
"""

import requests
import time
from urllib.parse import urljoin

# Базовый URL GitHub Pages
BASE_URL = "https://darksaiders12.github.io/upwork-proposal-generator/"

# Список страниц для проверки
PAGES_TO_CHECK = [
    "",  # Главная страница
    "index.html",
    "terms.html",
    "legal.html", 
    "privacy.html",
    "refund.html",
    "delivery-info.html"
]

def check_page(url, page_name):
    """Проверяет доступность страницы"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {page_name}: Доступна (HTTP {response.status_code})")
            return True
        else:
            print(f"❌ {page_name}: Ошибка HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {page_name}: Ошибка подключения - {e}")
        return False

def main():
    """Основная функция проверки"""
    print("🚀 Проверка статуса GitHub Pages")
    print("=" * 50)
    print(f"Базовый URL: {BASE_URL}")
    print()
    
    successful_checks = 0
    total_checks = len(PAGES_TO_CHECK)
    
    for page in PAGES_TO_CHECK:
        page_name = page if page else "Главная страница"
        url = urljoin(BASE_URL, page)
        
        if check_page(url, page_name):
            successful_checks += 1
        
        # Небольшая пауза между запросами
        time.sleep(1)
    
    print()
    print("=" * 50)
    print(f"Результат: {successful_checks}/{total_checks} страниц доступны")
    
    if successful_checks == total_checks:
        print("🎉 Все страницы успешно загружены на GitHub Pages!")
        print("\n📋 Готовые ссылки для анкеты ЮKassa:")
        print(f"• Главная страница: {BASE_URL}")
        print(f"• Пользовательское соглашение: {urljoin(BASE_URL, 'terms.html')}")
        print(f"• Реквизиты: {urljoin(BASE_URL, 'legal.html')}")
        print(f"• Политика конфиденциальности: {urljoin(BASE_URL, 'privacy.html')}")
        print(f"• Политика возвратов: {urljoin(BASE_URL, 'refund.html')}")
        print(f"• Способ получения услуги: {urljoin(BASE_URL, 'delivery-info.html')}")
    else:
        print("⚠️ Некоторые страницы недоступны. Проверьте настройки GitHub Pages.")
    
    print("\n🔗 Проверьте настройки GitHub Pages:")
    print("https://github.com/DARKSAIDERS12/upwork-proposal-generator/settings/pages")

if __name__ == "__main__":
    main() 