#!/usr/bin/env python3
"""
Русская премиум AI система для Upwork Proposal Generator
Интеграция Yandex GPT в премиум подписку
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from datetime import datetime
from alternative_ai_providers import YandexGPTProvider, GigaChatProvider, DemoProvider


class RussianPremiumAI:
    """Премиум AI система для российских пользователей"""
    
    def __init__(self):
        self.subscription_tiers = {
            'free': {
                'daily_limit': 3,
                'ai_provider': 'demo',
                'quality': 'basic',
                'features': ['basic_templates', 'demo_generation']
            },
            'premium': {
                'daily_limit': 50,
                'ai_provider': 'yandex',
                'quality': 'high',
                'features': ['premium_templates', 'yandex_gpt', 'priority_support', 'export']
            },
            'pro': {
                'daily_limit': 200,
                'ai_provider': 'yandex',
                'quality': 'high',
                'features': ['all_templates', 'yandex_gpt', 'gigachat_backup', 'priority_support', 'export', 'analytics']
            },
            'enterprise': {
                'daily_limit': -1,  # Unlimited
                'ai_provider': 'yandex',
                'quality': 'highest',
                'features': ['all_templates', 'yandex_gpt', 'gigachat_backup', 'dedicated_support', 'export', 'analytics', 'api_access']
            }
        }
        
        self.pricing = {
            'premium': {'price': 1500, 'currency': 'RUB', 'period': 'month'},  # ~$15
            'pro': {'price': 3000, 'currency': 'RUB', 'period': 'month'},      # ~$30
            'enterprise': {'price': 9900, 'currency': 'RUB', 'period': 'month'} # ~$99
        }
    
    def get_ai_provider_for_subscription(self, subscription_type: str) -> Optional[object]:
        """Возвращает AI провайдер для типа подписки"""
        
        if subscription_type not in self.subscription_tiers:
            subscription_type = 'free'
        
        tier = self.subscription_tiers[subscription_type]
        provider_type = tier['ai_provider']
        
        if provider_type == 'demo':
            return DemoProvider("demo")
        
        elif provider_type == 'yandex':
            api_key = self._get_yandex_api_key()
            if api_key:
                return YandexGPTProvider(api_key)
            else:
                # Fallback to demo if no API key
                return DemoProvider("demo")
        
        else:
            # Default fallback
            return DemoProvider("demo")
    
    def _get_yandex_api_key(self) -> Optional[str]:
        """Получает Yandex API ключ из конфигурации"""
        # Сначала проверяем переменную окружения
        api_key = os.getenv('YANDEX_API_KEY')
        if api_key and api_key != 'your-yandex-api-key-here':
            return api_key
        
        # Затем проверяем .env файл
        env_file = os.path.join('backend', '.env')
        if os.path.exists(env_file):
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('YANDEX_API_KEY='):
                        key = line.split('=', 1)[1].strip()
                        if key and key != 'your-yandex-api-key-here':
                            return key
        
        return None
    
    def generate_premium_proposal(self, user_id: int, subscription_type: str, 
                                project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует предложение с учетом премиум подписки"""
        
        # Проверяем ограничения подписки
        limits_check = self.check_subscription_limits(user_id, subscription_type)
        if not limits_check['can_generate']:
            return limits_check
        
        # Получаем AI провайдер
        ai_provider = self.get_ai_provider_for_subscription(subscription_type)
        if not ai_provider:
            return {
                'success': False,
                'error': 'AI провайдер недоступен',
                'error_code': 'PROVIDER_UNAVAILABLE'
            }
        
        # Добавляем премиум параметры к запросу
        enhanced_project_data = self._enhance_project_data(project_data, subscription_type)
        
        try:
            # Генерируем предложение
            proposal = ai_provider.generate_proposal(enhanced_project_data)
            
            # Инкрементируем счетчик использования
            self._increment_usage_counter(user_id)
            
            # Возвращаем результат с информацией о подписке
            return {
                'success': True,
                'proposal': proposal,
                'subscription_type': subscription_type,
                'ai_provider': self.subscription_tiers[subscription_type]['ai_provider'],
                'quality': self.subscription_tiers[subscription_type]['quality'],
                'daily_remaining': self._get_daily_remaining(user_id, subscription_type),
                'features_used': self.subscription_tiers[subscription_type]['features']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Ошибка генерации: {str(e)}',
                'error_code': 'GENERATION_ERROR'
            }
    
    def _enhance_project_data(self, project_data: Dict[str, Any], subscription_type: str) -> Dict[str, Any]:
        """Улучшает данные проекта в зависимости от подписки"""
        enhanced_data = project_data.copy()
        
        # Добавляем премиум параметры
        if subscription_type in ['premium', 'pro', 'enterprise']:
            enhanced_data['premium_mode'] = True
            enhanced_data['detailed_analysis'] = True
            enhanced_data['professional_tone'] = True
            
        if subscription_type in ['pro', 'enterprise']:
            enhanced_data['advanced_features'] = True
            enhanced_data['market_analysis'] = True
            
        if subscription_type == 'enterprise':
            enhanced_data['enterprise_features'] = True
            enhanced_data['custom_templates'] = True
            
        return enhanced_data
    
    def check_subscription_limits(self, user_id: int, subscription_type: str) -> Dict[str, Any]:
        """Проверяет лимиты подписки"""
        if subscription_type not in self.subscription_tiers:
            subscription_type = 'free'
        
        tier = self.subscription_tiers[subscription_type]
        daily_limit = tier['daily_limit']
        
        # Для unlimited подписок
        if daily_limit == -1:
            return {
                'can_generate': True,
                'subscription_type': subscription_type,
                'daily_remaining': 'unlimited'
            }
        
        # Проверяем текущее использование
        daily_used = self._get_daily_usage(user_id)
        
        if daily_used >= daily_limit:
            return {
                'can_generate': False,
                'reason': f'Превышен дневной лимит ({daily_limit} предложений)',
                'subscription_type': subscription_type,
                'daily_remaining': 0,
                'upgrade_required': subscription_type == 'free'
            }
        
        return {
            'can_generate': True,
            'subscription_type': subscription_type,
            'daily_remaining': daily_limit - daily_used
        }
    
    def _get_daily_usage(self, user_id: int) -> int:
        """Получает количество использований за день"""
        # Заглушка - в реальной системе это будет запрос к БД
        # TODO: Интегрировать с базой данных
        return 0
    
    def _increment_usage_counter(self, user_id: int):
        """Увеличивает счетчик использования"""
        # Заглушка - в реальной системе это будет обновление БД
        # TODO: Интегрировать с базой данных
        pass
    
    def _get_daily_remaining(self, user_id: int, subscription_type: str) -> Any:
        """Получает количество оставшихся генераций"""
        tier = self.subscription_tiers[subscription_type]
        daily_limit = tier['daily_limit']
        
        if daily_limit == -1:
            return 'unlimited'
        
        daily_used = self._get_daily_usage(user_id)
        return max(0, daily_limit - daily_used)
    
    def get_subscription_features(self, subscription_type: str) -> Dict[str, Any]:
        """Возвращает функции подписки"""
        if subscription_type not in self.subscription_tiers:
            subscription_type = 'free'
        
        tier = self.subscription_tiers[subscription_type]
        pricing = self.pricing.get(subscription_type, {})
        
        return {
            'subscription_type': subscription_type,
            'daily_limit': tier['daily_limit'],
            'ai_provider': tier['ai_provider'],
            'quality': tier['quality'],
            'features': tier['features'],
            'pricing': pricing
        }
    
    def get_upgrade_options(self, current_subscription: str) -> Dict[str, Any]:
        """Возвращает варианты апгрейда"""
        upgrade_options = {}
        
        subscription_order = ['free', 'premium', 'pro', 'enterprise']
        current_index = subscription_order.index(current_subscription) if current_subscription in subscription_order else 0
        
        for i, subscription in enumerate(subscription_order):
            if i > current_index:
                upgrade_options[subscription] = {
                    'features': self.get_subscription_features(subscription),
                    'upgrade_available': True
                }
        
        return upgrade_options
    
    def create_yandex_setup_instructions(self) -> Dict[str, Any]:
        """Создает инструкции по настройке Yandex GPT"""
        return {
            'title': '🚀 Настройка Yandex GPT для премиум подписки',
            'steps': [
                {
                    'step': 1,
                    'title': 'Регистрация в Yandex Cloud',
                    'description': 'Перейдите на https://cloud.yandex.ru/ и создайте аккаунт',
                    'url': 'https://cloud.yandex.ru/'
                },
                {
                    'step': 2,
                    'title': 'Активация Yandex GPT',
                    'description': 'В консоли Yandex Cloud активируйте сервис Yandex GPT',
                    'note': 'Может потребоваться привязка банковской карты'
                },
                {
                    'step': 3,
                    'title': 'Создание API ключа',
                    'description': 'Создайте API ключ в разделе "Сервисные аккаунты"',
                    'format': 'AQVN...'
                },
                {
                    'step': 4,
                    'title': 'Настройка в проекте',
                    'description': 'Запустите скрипт настройки и выберите Yandex GPT',
                    'command': 'python3 setup_russian_ai.py'
                }
            ],
            'benefits': [
                '✅ Высокое качество генерации',
                '✅ Поддержка русского языка',
                '✅ Низкая стоимость (~$0.001 за 1K токенов)',
                '✅ Полная легальность в России',
                '✅ Отсутствие блокировок'
            ],
            'cost_estimate': {
                'per_1k_tokens': '~0.08 RUB',
                'per_proposal': '~2-5 RUB',
                'monthly_for_50_proposals': '~100-250 RUB'
            }
        }


# Глобальный экземпляр
russian_premium_ai = RussianPremiumAI()


def test_russian_premium_ai():
    """Тестирование русской премиум AI системы"""
    print("🧪 Тестирование Russian Premium AI системы...")
    
    # Тест функций подписки
    for subscription_type in ['free', 'premium', 'pro', 'enterprise']:
        features = russian_premium_ai.get_subscription_features(subscription_type)
        print(f"\n📋 {subscription_type.upper()}:")
        print(f"   Лимит: {features['daily_limit']}")
        print(f"   AI: {features['ai_provider']}")
        print(f"   Функции: {', '.join(features['features'])}")
    
    # Тест генерации (демо)
    test_data = {
        'title': 'Разработка веб-сайта',
        'description': 'Нужен современный адаптивный сайт',
        'budget': '50000-100000 RUB',
        'specialization': 'Веб-разработка',
        'tone': 'Профессиональный'
    }
    
    result = russian_premium_ai.generate_premium_proposal(1, 'free', test_data)
    print(f"\n🎯 Тест генерации: {'✅ Успешно' if result['success'] else '❌ Ошибка'}")
    
    # Тест инструкций
    instructions = russian_premium_ai.create_yandex_setup_instructions()
    print(f"\n📖 Инструкции созданы: {instructions['title']}")
    
    print("\n✅ Тестирование завершено!")


if __name__ == "__main__":
    test_russian_premium_ai()