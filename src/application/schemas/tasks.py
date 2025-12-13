from enum import Enum
from uuid import UUID
from src.application.schemas.common import BaseSchema


class CardUsecaseName(str, Enum):
    CREATE = "create_cards"
    UPDATE = "update_card"
    DELETE = "delete_card"
    GENERATE = "generate_cards"
    GET_ALL = "get_all_cards"


class DeleteCardTaskPayload(BaseSchema):
    id: UUID


class CardTaskRequest(BaseSchema):
    usecase: CardUsecaseName
    payload: dict | None = None


class CardTaskResponse(BaseSchema):
    task_id: str
    usecase: CardUsecaseName
    payload: dict | None = None
