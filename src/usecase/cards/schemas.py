from uuid import UUID
from pydantic import BaseModel
from src.application.schemas.cards import UpdateCardSchema


class GetUpdateCardsSchema(BaseModel):
    id: UUID
    card: UpdateCardSchema