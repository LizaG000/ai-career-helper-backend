from uuid import UUID
from datetime import datetime
from src.application.schemas.common import BaseModel

class CardSchema(BaseModel):
    id: UUID
    information_id: UUID
    title: str
    description: str
    created_at: datetime
    updated_at: datetime