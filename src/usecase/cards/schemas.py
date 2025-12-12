from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.application.schemas.cards import CreateCardSchema, UpdateCardSchema


class GetUpdateCardsSchema(BaseModel):
    id: UUID
    card: UpdateCardSchema


class CardSchema(BaseModel):
    id: UUID
    title: str
    description: str
    created_at: datetime


class CardsSchema(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    cards: list[CardSchema]


class ResponseCardsSchema(BaseModel):
    items: list[CardsSchema]
    next: str | None = None
    prev: str | None = None
    total: int


class PaginationSchema(BaseModel):
    limit: int
    offset: int


class CreateManyCardsSchema(BaseModel):
    cards: list[CreateCardSchema]
