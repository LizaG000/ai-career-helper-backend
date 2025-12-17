from dataclasses import dataclass
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import UpdateReturningGate
from src.application.schemas.user_careers import UserCareersSchema, UpdateUserCareerSchema
from src.usecase.user_careers.schemas import GetUpdateUserCareersSchema
from src.infra.postgres.tables import UserCareersModel

@dataclass(slots=True, frozen=True, kw_only=True)
class UpdateUserCareer(Usecase[GetUpdateUserCareersSchema, UserCareersSchema]):
    session: AsyncSession
    update_user_career: UpdateReturningGate[UserCareersModel, UpdateUserCareerSchema, UUID, UserCareersSchema]

    async def __call__(self, data: GetUpdateUserCareersSchema) -> UserCareersSchema:
        async with self.session.begin():
            return await self.update_user_career(entity_id=data.id, entity=data.user_career)
