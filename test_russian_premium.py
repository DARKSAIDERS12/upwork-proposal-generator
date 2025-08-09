#!/usr/bin/env python3
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
