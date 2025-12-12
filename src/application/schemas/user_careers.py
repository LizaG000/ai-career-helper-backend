from datetime import datetime
from uuid import UUID

from src.application.schemas.common import BaseModel


class UserCareersSchema(BaseModel):
    id: UUID
    user_id: UUID
    specialization_id: UUID | None
    experience_level: str
    skills: str
    career_goal: str
    updated_at: datetime
    created_at: datetime


class CreateUserCareersSchema(BaseModel):
    user_id: UUID
    specialization_id: UUID | None
    experience_level: str
    skills: str
    career_goal: str
