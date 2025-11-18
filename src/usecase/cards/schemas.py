from uuid import UUID
from pydantic import BaseModel
from src.application.schemas.cards import UpdateCardSchema, CreateCardSchema


class GetUpdateCardsSchema(BaseModel):
    id: UUID
    card: UpdateCardSchema


class CreateManyCardsSchema(BaseModel):
    cards: list[CreateCardSchema]