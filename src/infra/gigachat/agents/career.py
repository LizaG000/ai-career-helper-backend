import pdfplumber
from src.infra.gigachat.base import BaseAgent
from io import BytesIO

class CareerAgent(BaseAgent):
    def __init__(self):
        tools = [
            self.analyze_resume_tool,
            self.analyze_vacancy_tool,
            self.generate_interview_questions_tool,
            self.extract_pdf_text_tool,
        ]
        super().__init__("career_agent", tools)


    def extract_pdf_text_tool(self, pdf_path: bytes) -> str:
        """Извлекает текст из PDF файла"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text[:2000]
        except Exception as e:
            return f"Ошибка при чтении PDF: {str(e)}"

    def analyze_resume_tool(self, pdf: bytes | None) -> str:
        """Анализирует резюме из PDF файла"""
        if pdf is None:
            return "📂 Пришли свое резюме!!!"
        with pdfplumber.open(BytesIO(pdf)) as pdf:
            total_pages = len(pdf.pages)

            for page_num, page in enumerate(pdf.pages, 1):
                # Извлекаем текст со страницы
                text = page.extract_text()

        prompt = f"""
        Проанализируй это резюме и дай рекомендации по улучшению:

        {text}

        Критерии анализа:
        1. Структура и читаемость
        2. Наличие конкретных достижений и метрик
        3. Соответствие современным требованиям
        4. Оптимизация под ATS системы
        5. Профессиональное впечатление

        Верни структурированный анализ.
        """

        response = self.model.chat(prompt)
        return response.choices[0].message.content

    def analyze_vacancy_tool(self, pdf_path: str) -> str:
        """Анализирует вакансию из PDF файла"""
        text = self.extract_pdf_text_tool(pdf_path)
        # доставать из файла
        prompt = f"""
        Проанализируй вакансию и определи "красные флаги":

        {text}

        Ищи:
        1. Размытые обязанности
        2. Непрозрачные условия оплаты
        3. Завышенные требования
        4. Признаки токсичной рабочей среды
        5. Противоречивые условия

        Верни анализ с выделением позитивных и негативных аспектов.
        """

        response = self.model.chat(prompt)
        return response.choices[0].message.content

    def generate_interview_questions_tool(self, position: str, level: str = "middle") -> str:
        """Генерирует вопросы для собеседования"""

        # доставать из файла
        prompt = f"""
        Сгенерируй список из 10-15 вопросов для собеседования на позицию {position} уровня {level}.
        Включи:
        - Технические вопросы
        - Поведенческие вопросы
        - Вопросы о мотивации
        - Кейсовые задания

        Для каждого вопроса укажи, на что обращать внимание в ответе.
        """

        response = self.model.chat(prompt)
        return response.choices[0].message.content


    async def __call__(self, query: str):
        q = query.lower()
        if "собеседован" in q and "вопрос" in q:
            resp_text =  self.generate_interview_questions_tool(position=query)

        elif "ваканси" in q and ".pdf" not in q:
            prompt = (
                f"Проанализируй эту вакансию и укажи красные и зелёные флаги.\n\n"
                f"Текст запроса пользователя:\n{query}"
            )
            resp_text = self.chat(prompt)

        else:
            # Всё остальное по карьере — просто отдаём LLM с историей
            resp_text = self.chat(query)
        return resp_text
