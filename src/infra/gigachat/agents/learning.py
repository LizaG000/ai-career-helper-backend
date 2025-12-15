import pdfplumber
from src.infra.gigachat.base import BaseAgent
from io import BytesIO

class LearningAgent(BaseAgent):
    def __init__(self):
        tools = [
            self.create_roadmap_tool,
            self.recommend_materials_tool,
            self.explain_concept_tool,
            self.extract_pdf_text_tool,
        ]
        super().__init__("learning_agent", tools)

    def extract_pdf_text_tool(self, pdf: bytes) -> str:
        """Извлекает текст из PDF файла"""
        try:
            text = ""
            with pdfplumber.open(pdf) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text[:2000]
        except Exception as e:
            return f"Ошибка при чтении PDF: {str(e)}"

    def create_roadmap_tool(self, profession: str,) -> str:
        """Создает образовательный roadmap"""
        prompt = f"""
        Изучи запрос пользователя и определи из его запроса на какой срок будет создаваться учебный план.
        Создай детальный образовательный roadmap для профессии {profession} на период, который ты определил из запроса ранее

        Структура:
        1. Цели обучения
        2. Поэтапный план (с временными метками)
        3. Ключевые навыки для освоения
        4. Рекомендуемые проекты для практики
        5. Метрики успеха
        6. Чекпоинты для самопроверки

        Сделай roadmap практичным и достижимым.
        """

        response = self.model.chat(prompt)
        return response.choices[0].message.content

    def recommend_materials_tool(self, topic: str, level: str = "beginner") -> str:
        """Рекомендует обучающие материалы"""
        prompt = f"""
        Подбери рекомендации обучающих материалов по теме {topic} для уровня {level}.

        Включи:
        - Книги (с обоснованием выбора)
        - Онлайн курсы
        - Статьи и блоги
        - Видео материалы
        - Практические задания
        - Сообщества для обучения

        Укажи примерное время на освоение каждого ресурса.
        """

        response = self.model.chat(prompt)
        return response.choices[0].message.content

    def explain_concept_tool(self, concept: str, explanation_level: str = "новичок") -> str:
        """Объясняет сложные концепции простым языком"""
        prompt = f"""
        Объясни концепцию {concept} для уровня {explanation_level}.

        Используй:
        - Простые аналогии
        - Конкретные примеры
        - Визуальные метафоры
        - Практические применения

        Избегай сложной терминологии, объясняй как для новичка.
        """

        response = self.model.chat(prompt)
        return response.choices[0].message.content


    async def __call__(self, query: str):
        q = query.lower()
        if "roadmap" in q or "дорожн" in q or "план" in q:
            resp_text = self.create_roadmap_tool(profession=query)

        elif "объясн" in q or "концепц" in q:
            resp_text = self.explain_concept_tool(concept=query)

        else:
            resp_text = self.chat(query)
        return resp_text