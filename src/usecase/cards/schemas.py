from uuid import UUID
from pydantic import BaseModel
from src.application.schemas.cards import UpdateCardSchema
from datetime import datetime
from src.application.schemas.cards import CardSchema

class GetUpdateCardsSchema(BaseModel):
    id: UUID
    card: UpdateCardSchema

class CardsSchema(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    cards: list[CardSchema]

class PaginationSchema(BaseModel):
    limit: int
    offset: int