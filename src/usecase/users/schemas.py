from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from src.application.schemas.users import UpdateUserSchema
class GetUpdateUserSchema(BaseModel):
    id: UUID
    user: UpdateUserSchema