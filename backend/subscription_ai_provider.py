#!/usr/bin/env python3
"""
AI провайдер с учетом подписок и лимитов
"""

import os
import sys
from typing import Dict, Any, Optional
from alternative_ai_providers import get_ai_provider, DemoProvider

class SubscriptionAIProvider:
    """AI провайдер с учетом подписок"""
    
    def __init__(self):
        self.payment_system = None
        try:
            from payment_system import payment_system
            self.payment_system = payment_system
        except ImportError:
            print("⚠️  Система платежей не найдена, используется демо-режим")
    
    def generate_proposal(self, user_id: int, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует предложение с учетом подписки пользователя"""
        
        # Проверяем, может ли пользователь генерировать предложения
        if self.payment_system:
            can_generate = self.payment_system.can_generate_proposal(user_id)
            
            if not can_generate['can_generate']:
                return {
                    'success': False,
                    'error': can_generate['reason'],
                    'subscription': can_generate['subscription'],
                    'upgrade_required': can_generate.get('upgrade_required', False)
                }
        
        # Определяем, какой AI провайдер использовать
        ai_provider = self._get_ai_provider_for_user(user_id)
        
        # Генерируем предложение
        try:
            proposal = ai_provider.generate_proposal(project_data)
            
            # Увеличиваем счетчик предложений
            if self.payment_system:
                self.payment_system.increment_proposal_count(user_id)
            
            return {
                'success': True,
                'proposal': proposal,
                'subscription': self._get_user_subscription_type(user_id),
                'daily_remaining': self._get_daily_remaining(user_id)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Ошибка генерации: {str(e)}'
            }
    
    def _get_ai_provider_for_user(self, user_id: int):
        """Возвращает подходящий AI провайдер для пользователя"""
        
        subscription_status = self._get_user_subscription_status(user_id)
        
        # Для премиум пользователей используем реальный AI
        if subscription_status == 'premium':
            # Получаем настройки из .env
            ai_provider = os.getenv('AI_PROVIDER', 'demo')
            
            if ai_provider in ['yandex', 'gigachat', 'openai']:
                # Проверяем, есть ли API ключ
                api_key = self._get_api_key_for_provider(ai_provider)
                if api_key and api_key != 'demo_key':
                    try:
                        return get_ai_provider(ai_provider, api_key)
                    except Exception as e:
                        print(f"Ошибка инициализации {ai_provider}: {e}")
        
        # Для всех остальных используем демо-режим
        return DemoProvider("demo")
    
    def _get_user_subscription_status(self, user_id: int) -> str:
        """Получает статус подписки пользователя"""
        if self.payment_system:
            return self.payment_system.get_user_subscription_status(user_id)
        return 'free'
    
    def _get_user_subscription_type(self, user_id: int) -> str:
        """Получает тип подписки пользователя"""
        status = self._get_user_subscription_status(user_id)
        return status
    
    def _get_daily_remaining(self, user_id: int) -> Optional[int]:
        """Получает количество оставшихся предложений на сегодня"""
        if self.payment_system:
            can_generate = self.payment_system.can_generate_proposal(user_id)
            return can_generate.get('daily_remaining')
        return None
    
    def _get_api_key_for_provider(self, provider: str) -> Optional[str]:
        """Получает API ключ для провайдера"""
        env_file = os.path.join('backend', '.env')
        
        if os.path.exists(env_file):
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if provider == 'yandex':
                for line in content.split('\n'):
                    if line.startswith('YANDEX_API_KEY='):
                        return line.split('=', 1)[1].strip()
            
            elif provider == 'gigachat':
                for line in content.split('\n'):
                    if line.startswith('GIGACHAT_API_KEY='):
                        return line.split('=', 1)[1].strip()
            
            elif provider == 'openai':
                for line in content.split('\n'):
                    if line.startswith('OPENAI_API_KEY='):
                        key = line.split('=', 1)[1].strip()
                        if key.startswith('sk-'):
                            return key
        
        return None
    
    def get_subscription_info(self, user_id: int) -> Dict[str, Any]:
        """Получает информацию о подписке пользователя"""
        if not self.payment_system:
            return {
                'subscription': 'free',
                'features': self._get_free_features(),
                'upgrade_available': True
            }
        
        subscription_status = self._get_user_subscription_status(user_id)
        
        if subscription_status == 'premium':
            return {
                'subscription': 'premium',
                'features': self._get_premium_features(),
                'upgrade_available': False,
                'can_cancel': True
            }
        else:
            return {
                'subscription': 'free',
                'features': self._get_free_features(),
                'upgrade_available': True,
                'daily_remaining': self._get_daily_remaining(user_id)
            }
    
    def _get_free_features(self) -> Dict[str, Any]:
        """Возвращает функции бесплатной версии"""
        return {
            'daily_proposals': 3,
            'ai_provider': 'demo',
            'templates': 'basic',
            'support': 'community',
            'export': False,
            'priority': False
        }
    
    def _get_premium_features(self) -> Dict[str, Any]:
        """Возвращает функции премиум версии"""
        return {
            'daily_proposals': 'unlimited',
            'ai_provider': 'advanced',
            'templates': 'premium',
            'support': 'priority',
            'export': True,
            'priority': True
        }

# Глобальный экземпляр
subscription_ai = SubscriptionAIProvider() 