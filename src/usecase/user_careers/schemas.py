from uuid import UUID
from pydantic import BaseModel
from src.application.schemas.user_careers import UpdateUserCareersSchema
class GetUpdateUserCareersSchema(BaseModel):
    id: UUID
    usercareer: UpdateUserCareersSchema