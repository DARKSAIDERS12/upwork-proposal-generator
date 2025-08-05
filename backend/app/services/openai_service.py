import time
from typing import Dict, Any, Optional
from openai import OpenAI
from ..config import settings

class OpenAIService:
    def __init__(self):
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key not configured")
        
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def generate_proposal(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует предложение на основе данных проекта"""
        start_time = time.time()
        
        # Создаем промпт на основе данных проекта
        prompt = self._create_proposal_prompt(project_data)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Ты эксперт по написанию выигрышных предложений для фрилансеров на Upwork. Твоя задача - создавать персонализированные, профессиональные и убедительные предложения, которые помогут фрилансерам получить проект."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            generation_time = int(time.time() - start_time)
            
            return {
                "content": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "generation_time": generation_time,
                "model": response.model
            }
            
        except Exception as e:
            raise Exception(f"Error generating proposal: {str(e)}")
    
    def _create_proposal_prompt(self, project_data: Dict[str, Any]) -> str:
        """Создает промпт для генерации предложения"""
        
        specialization = project_data.get("specialization", "Общая специализация")
        experience_level = project_data.get("experience_level", "1-2 года")
        budget_range = project_data.get("budget_range", "$100-500")
        project_description = project_data.get("project_description", "")
        key_requirements = project_data.get("key_requirements", "")
        tone = project_data.get("tone", "профессиональный")
        
        # Определяем тон письма
        tone_instruction = {
            "формальный": "Используй формальный, деловой тон",
            "дружелюбный": "Используй дружелюбный, но профессиональный тон",
            "профессиональный": "Используй профессиональный, уверенный тон"
        }.get(tone, "Используй профессиональный тон")
        
        prompt = f"""
        Создай выигрышное предложение для проекта на Upwork.
        
        {tone_instruction}.
        
        Информация о проекте:
        - Описание: {project_description}
        - Бюджет: {budget_range}
        - Специализация: {specialization}
        - Ключевые требования: {key_requirements}
        
        Информация о фрилансере:
        - Опыт: {experience_level}
        - Специализация: {specialization}
        
        Структура предложения:
        1. Приветствие и заинтересованность в проекте
        2. Краткое представление опыта и экспертизы
        3. Понимание задачи и предложение решения
        4. Конкретные примеры работ или подходов
        5. Вопросы для уточнения деталей
        6. Призыв к действию
        
        Предложение должно быть:
        - Персонализированным под конкретный проект
        - Показывать понимание задачи
        - Демонстрировать экспертизу
        - Быть убедительным, но не навязчивым
        - Длиной 200-300 слов
        
        Создай предложение:
        """
        
        return prompt
    
    def generate_multiple_proposals(self, project_data: Dict[str, Any], count: int = 3) -> list:
        """Генерирует несколько вариантов предложений"""
        proposals = []
        
        for i in range(count):
            # Меняем тон для разнообразия
            tones = ["профессиональный", "дружелюбный", "формальный"]
            project_data["tone"] = tones[i % len(tones)]
            
            proposal = self.generate_proposal(project_data)
            proposals.append(proposal)
        
        return proposals 