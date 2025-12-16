from uuid import UUID
from datetime import datetime
from src.application.schemas.common import BaseModel

class ChatSchemas(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    start_time: datetime
    last_activity_time: datetime
    created_at: datetime
    updated_at: datetime

class CreateChatSchema(BaseModel):
    user_id: UUID
    title: str
