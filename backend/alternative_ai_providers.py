#!/usr/bin/env python3
"""
Альтернативные AI провайдеры для работы из России
"""

import os
import requests
import json
from typing import Dict, Any, Optional

class AIProvider:
    """Базовый класс для AI провайдеров"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def generate_proposal(self, project_data: Dict[str, Any]) -> str:
        """Генерирует предложение на основе данных проекта"""
        raise NotImplementedError

class YandexGPTProvider(AIProvider):
    """Yandex GPT - российский аналог OpenAI"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    def generate_proposal(self, project_data: Dict[str, Any]) -> str:
        """Генерирует предложение используя Yandex GPT"""
        
        prompt = self._create_prompt(project_data)
        
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "modelUri": "gpt://b1g8c7c7c7c7c7c7c7c7c/yandexgpt-lite",
            "completionOptions": {
                "temperature": 0.7,
                "maxTokens": 1000
            },
            "messages": [
                {
                    "role": "user",
                    "text": prompt
                }
            ]
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result["result"]["alternatives"][0]["message"]["text"]
            
        except Exception as e:
            return f"Ошибка генерации: {str(e)}"
    
    def _create_prompt(self, project_data: Dict[str, Any]) -> str:
        """Создает промпт для генерации предложения"""
        
        return f"""
        Создай профессиональное предложение для проекта на Upwork.
        
        Детали проекта:
        - Название: {project_data.get('title', 'Не указано')}
        - Описание: {project_data.get('description', 'Не указано')}
        - Бюджет: {project_data.get('budget', 'Не указан')}
        - Специализация: {project_data.get('specialization', 'Не указана')}
        - Тон: {project_data.get('tone', 'Профессиональный')}
        
        Создай убедительное предложение, которое:
        1. Показывает понимание проекта
        2. Демонстрирует опыт в данной области
        3. Объясняет подход к решению задачи
        4. Включает конкретные примеры работ
        5. Завершается призывом к действию
        
        Предложение должно быть на английском языке, профессиональным и убедительным.
        """

class GigaChatProvider(AIProvider):
    """GigaChat - российский AI от Сбера"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    
    def generate_proposal(self, project_data: Dict[str, Any]) -> str:
        """Генерирует предложение используя GigaChat"""
        
        prompt = self._create_prompt(project_data)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "GigaChat:latest",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            return f"Ошибка генерации: {str(e)}"
    
    def _create_prompt(self, project_data: Dict[str, Any]) -> str:
        """Создает промпт для генерации предложения"""
        
        return f"""
        Создай профессиональное предложение для проекта на Upwork.
        
        Детали проекта:
        - Название: {project_data.get('title', 'Не указано')}
        - Описание: {project_data.get('description', 'Не указано')}
        - Бюджет: {project_data.get('budget', 'Не указан')}
        - Специализация: {project_data.get('specialization', 'Не указана')}
        - Тон: {project_data.get('tone', 'Профессиональный')}
        
        Создай убедительное предложение, которое:
        1. Показывает понимание проекта
        2. Демонстрирует опыт в данной области
        3. Объясняет подход к решению задачи
        4. Включает конкретные примеры работ
        5. Завершается призывом к действию
        
        Предложение должно быть на английском языке, профессиональным и убедительным.
        """

class DemoProvider(AIProvider):
    """Демо-провайдер для тестирования без API"""
    
    def generate_proposal(self, project_data: Dict[str, Any]) -> str:
        """Генерирует демо-предложение"""
        
        title = project_data.get('title', 'Web Development Project')
        budget = project_data.get('budget', '$500-1000')
        specialization = project_data.get('specialization', 'Web Development')
        
        return f"""
Dear Client,

I've reviewed your project "{title}" and I'm excited about the opportunity to work with you. With my extensive experience in {specialization}, I'm confident I can deliver exceptional results that exceed your expectations.

**Why I'm the right fit for your project:**

✅ **Proven Expertise**: I have successfully completed 50+ similar projects with 5-star ratings
✅ **Quality Assurance**: Every deliverable goes through rigorous testing and review
✅ **Clear Communication**: Regular updates and transparent project management
✅ **On-time Delivery**: 100% on-time completion rate with all my clients

**My approach to your project:**
1. Detailed analysis of requirements and objectives
2. Custom solution design tailored to your specific needs
3. Iterative development with regular feedback cycles
4. Thorough testing and quality assurance
5. Comprehensive documentation and support

**Budget**: I can work within your {budget} budget while ensuring top-quality results.

**Timeline**: I can start immediately and deliver within your required timeframe.

I'm ready to begin working on your project right away. Let's discuss the details and get started!

Best regards,
[Your Name]
Freelance {specialization} Expert

P.S. I'm available for a quick call to discuss your project in detail.
        """

def get_ai_provider(provider_name: str, api_key: str) -> AIProvider:
    """Возвращает AI провайдера по названию"""
    
    providers = {
        "yandex": YandexGPTProvider,
        "gigachat": GigaChatProvider,
        "demo": DemoProvider
    }
    
    provider_class = providers.get(provider_name.lower())
    if not provider_class:
        raise ValueError(f"Неизвестный провайдер: {provider_name}")
    
    return provider_class(api_key)

def test_providers():
    """Тестирует доступность различных провайдеров"""
    
    print("🧪 Тестирование AI провайдеров...")
    
    # Тестовые данные
    test_data = {
        "title": "Website Development",
        "description": "Need a modern responsive website",
        "budget": "$1000-2000",
        "specialization": "Web Development",
        "tone": "Professional"
    }
    
    # Тестируем демо-провайдер
    try:
        demo_provider = DemoProvider("demo")
        result = demo_provider.generate_proposal(test_data)
        print("✅ Демо-провайдер работает")
        print(f"Результат: {result[:100]}...")
    except Exception as e:
        print(f"❌ Демо-провайдер не работает: {e}")
    
    print("\n📋 Доступные провайдеры:")
    print("1. demo - Демо-режим (работает без API)")
    print("2. yandex - Yandex GPT (требует API ключ)")
    print("3. gigachat - GigaChat (требует API ключ)")

if __name__ == "__main__":
    test_providers() 