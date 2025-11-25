from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
#from src.application.schemas.cards import UpdateCardSchema, CreateCardSchema
from src.application.schemas.user_careers import UpdateUserCareerSchema
class UserCareerSchema(BaseModel):
    id: UUID
    title: str
    description: str
    created_at: datetime
    id: UUID
    experience_level: str
    skills: str
    career_goal: str
    created_at: datetime
class UserCareersSchema(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    cards: list[UserCareerSchema]
class GetUpdateUserCareersSchema(BaseModel):
    id: UUID
    user_career: UpdateUserCareerSchema