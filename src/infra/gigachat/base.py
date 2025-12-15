from typing import Dict, Any, List, Optional
from gigachat import GigaChat, GigaChatAsyncClient
from src.main.config import config


class BaseAgent:
    def __init__(self, name: str, tools: List[Any]):
        self.name = name
        self.tools = tools
        self.model = GigaChat(credentials=config.gigachat.authorization_key, verify_ssl_certs=False)

    def chat(self, user_query: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        if history:
            hist_text = ""
            # Берём только последние N сообщений, чтобы не раздуть контекст
            for msg in history[-10:]:
                role = "Пользователь" if msg["role"] == "user" else "Ассистент"
                hist_text += f"{role}: {msg['content']}\n"

            prompt = (
                f"{hist_text}\n"
                f"Пользователь: {user_query}\n"
                f"Ассистент:"
            )
        else:
            prompt = user_query

        resp = self.model.chat(prompt)
        return resp.choices[0].message.content