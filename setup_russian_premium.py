#!/usr/bin/env python3
"""
Автоматическая настройка русской премиум AI системы
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("🇷🇺 НАСТРОЙКА РУССКОЙ ПРЕМИУМ AI СИСТЕМЫ")
    print("=" * 60)
    print("Интеграция Yandex GPT в премиум подписку")
    print("=" * 60)

def check_files():
    """Проверяет наличие всех необходимых файлов"""
    print("\n📂 Проверка файлов...")
    
    required_files = [
        'backend/russian_premium_ai.py',
        'subscription_manager.html',
        'app.js',
        'index.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Отсутствуют файлы: {', '.join(missing_files)}")
        return False
    
    print("\n✅ Все файлы найдены!")
    return True

def test_russian_premium_ai():
    """Тестирует русскую премиум AI систему"""
    print("\n🧪 Тестирование Russian Premium AI...")
    
    try:
        # Добавляем backend в путь
        sys.path.append('backend')
        from russian_premium_ai import russian_premium_ai
        
        # Тест функций подписки
        for subscription_type in ['free', 'premium', 'pro', 'enterprise']:
            features = russian_premium_ai.get_subscription_features(subscription_type)
            print(f"✅ {subscription_type.upper()}: {features['daily_limit']} предложений/день")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

def create_subscription_pricing():
    """Создает файл с ценами в российских рублях"""
    pricing_data = {
        'currency': 'RUB',
        'plans': {
            'free': {
                'price': 0,
                'daily_limit': 3,
                'ai_provider': 'demo',
                'features': ['basic_templates', 'demo_generation']
            },
            'premium': {
                'price': 1500,
                'daily_limit': 50,
                'ai_provider': 'yandex',
                'features': ['premium_templates', 'yandex_gpt', 'priority_support', 'export']
            },
            'pro': {
                'price': 3000,
                'daily_limit': 200,
                'ai_provider': 'yandex',
                'features': ['all_templates', 'yandex_gpt', 'gigachat_backup', 'priority_support', 'export', 'analytics']
            },
            'enterprise': {
                'price': 9900,
                'daily_limit': -1,
                'ai_provider': 'all',
                'features': ['all_templates', 'all_ai_providers', 'dedicated_support', 'export', 'analytics', 'api_access']
            }
        }
    }
    
    with open('backend/pricing_config.json', 'w', encoding='utf-8') as f:
        json.dump(pricing_data, f, ensure_ascii=False, indent=2)
    
    print("✅ Создан файл pricing_config.json")

def update_backend_config():
    """Обновляет конфигурацию backend"""
    print("\n⚙️ Обновление конфигурации backend...")
    
    # Проверяем наличие .env файла
    env_file = 'backend/.env'
    if not os.path.exists(env_file):
        print("📝 Создание файла .env...")
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write("""# Russian Premium AI Configuration
AI_PROVIDER=demo
YANDEX_API_KEY=your-yandex-api-key-here
GIGACHAT_API_KEY=your-gigachat-api-key-here
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./upwork_proposals.db
ENABLE_RUSSIAN_PREMIUM=true
DEFAULT_SUBSCRIPTION=free
""")
        print("✅ Файл .env создан")
    else:
        print("✅ Файл .env уже существует")

def create_test_script():
    """Создает скрипт для тестирования системы"""
    test_script = """#!/usr/bin/env python3
import os
import sys
sys.path.append('backend')

from russian_premium_ai import russian_premium_ai

def test_subscription_system():
    print("🧪 Тестирование системы подписок...")
    
    # Тест всех планов
    for plan in ['free', 'premium', 'pro', 'enterprise']:
        features = russian_premium_ai.get_subscription_features(plan)
        print(f"✅ {plan}: {features['daily_limit']} предложений, AI: {features['ai_provider']}")
    
    # Тест генерации
    test_data = {
        'title': 'Тестовый проект',
        'description': 'Описание проекта',
        'budget': '50000 RUB',
        'specialization': 'Веб-разработка',
        'tone': 'Профессиональный'
    }
    
    result = russian_premium_ai.generate_premium_proposal(1, 'free', test_data)
    print(f"📝 Тест генерации: {'✅ Успешно' if result['success'] else '❌ Ошибка'}")
    
    print("✅ Тестирование завершено!")

if __name__ == "__main__":
    test_subscription_system()
"""
    
    with open('test_russian_premium.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    # Делаем файл исполняемым
    os.chmod('test_russian_premium.py', 0o755)
    print("✅ Создан скрипт test_russian_premium.py")

def create_quick_start_guide():
    """Создает краткое руководство по запуску"""
    guide = """# 🇷🇺 КРАТКОЕ РУКОВОДСТВО ПО РУССКОЙ ПРЕМИУМ СИСТЕМЕ

## ✅ Что настроено:

1. **Russian Premium AI система** - интеграция Yandex GPT в подписки
2. **Менеджер подписок** - subscription_manager.html
3. **Обновленный интерфейс** - поддержка русских AI провайдеров
4. **Ценообразование в рублях** - адаптировано для российского рынка

## 🚀 Быстрый запуск:

```bash
# 1. Запустите проект
python3 quick_start.py

# 2. Откройте сайт
# http://localhost:3000

# 3. Настройте Yandex GPT (для премиум)
# - Получите API ключ на cloud.yandex.ru
# - Нажмите "Настроить API" в интерфейсе
# - Введите ключ

# 4. Протестируйте систему
python3 test_russian_premium.py
```

## 💰 Тарифные планы:

- **FREE**: 3 предложения/день, демо-режим (0 RUB)
- **PREMIUM**: 50 предложений/день, Yandex GPT (1500 RUB/мес)
- **PRO**: 200 предложений/день, Yandex GPT + GigaChat (3000 RUB/мес)
- **ENTERPRISE**: Без лимитов, все AI провайдеры (9900 RUB/мес)

## 🛠 Что нужно сделать дальше:

1. Получить Yandex GPT API ключ
2. Настроить систему платежей (Stripe/ЮKassa)
3. Провести бета-тестирование
4. Запустить маркетинг

## 📞 Поддержка:

- Файлы конфигурации: backend/
- Документация: ИНСТРУКЦИЯ_ДЛЯ_РОССИИ.md
- Тестирование: test_russian_premium.py
"""
    
    with open('РУССКАЯ_ПРЕМИУМ_СИСТЕМА.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("✅ Создано руководство РУССКАЯ_ПРЕМИУМ_СИСТЕМА.md")

def main():
    print_banner()
    
    # Проверяем файлы
    if not check_files():
        print("\n❌ Не все файлы найдены. Запустите сначала основную настройку.")
        return
    
    # Тестируем Russian Premium AI
    if not test_russian_premium_ai():
        print("\n❌ Ошибка тестирования системы.")
        return
    
    # Создаем конфигурационные файлы
    create_subscription_pricing()
    update_backend_config()
    create_test_script()
    create_quick_start_guide()
    
    print("\n" + "=" * 60)
    print("🎉 РУССКАЯ ПРЕМИУМ СИСТЕМА НАСТРОЕНА!")
    print("=" * 60)
    
    print("\n📋 Следующие шаги:")
    print("1. Получите Yandex GPT API ключ на cloud.yandex.ru")
    print("2. Запустите проект: python3 quick_start.py")
    print("3. Откройте менеджер подписок: subscription_manager.html")
    print("4. Протестируйте: python3 test_russian_premium.py")
    
    print("\n💰 Тарифы настроены:")
    print("• FREE: 0 RUB (демо)")
    print("• PREMIUM: 1500 RUB (Yandex GPT)")  
    print("• PRO: 3000 RUB (Yandex GPT + GigaChat)")
    print("• ENTERPRISE: 9900 RUB (все AI провайдеры)")
    
    print("\n🔗 Полезные ссылки:")
    print("• Yandex Cloud: https://cloud.yandex.ru/")
    print("• GigaChat: https://developers.sber.ru/")
    print("• Сайт проекта: http://localhost:3000")
    
    print("\n🎯 ГОТОВО! Система готова к использованию!")

if __name__ == "__main__":
    main()