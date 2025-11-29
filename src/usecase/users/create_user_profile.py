from typing import Tuple, Dict, Any
from src.application.schemas.users import CreateUserSchema, UserResponse
from src.application.schemas.user_careers import UserCareerCreate, UserCareerResponse
from src.infra.postgres.gateways.base import UserGate, UserCareerGate
from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase import db
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateGate
from src.application.schemas.users import CreateUserSchema
from src.infra.postgres.tables import UserModel
from dataclasses import dataclass


class CreateUserProfileUseCase:
    def __init__(self):
        self.user_gate = UserGate()
        self.user_career_gate = UserCareerGate()

    async def execute(
        self, 
        user_data: CreateUserSchema, 
        career_data: UserCareerCreate
    ) -> Tuple[UserResponse, UserCareerResponse]:
        async with db.transaction():
            user = await self.user_gate.create(user_data)
            career_data_dict = career_data.dict()
            career_data_dict['user_id'] = user.id
            user_career = await self.user_career_gate.create(
                UserCareerCreate(**career_data_dict)
            )
            return user, user_career
        
