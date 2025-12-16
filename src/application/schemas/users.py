from uuid import UUID
from datetime import datetime
from src.application.schemas.common import BaseModel

class UserSchema(BaseModel):
    id: UUID
    email: str
    first_name: str
    corporate_account_id: UUID|None
    is_active: bool
    created_at: datetime
    updated_at: datetime

class CreateUserSchema(BaseModel):
    first_name: str
    email: str
    corporate_account_id: UUID|None
