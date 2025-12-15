from uuid import UUID
from datetime import datetime
from src.application.schemas.common import BaseModel

class MessageSchemas(BaseModel):
    id: UUID
    chat_id: UUID
    text: str
    sender_type_id: UUID
    created_at: datetime
    updated_at: datetime

class CreateMessageSchema(BaseModel):
    chat_id: UUID
    text: str
    sender_type_id: UUID
