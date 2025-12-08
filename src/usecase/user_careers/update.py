from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import UpdateReturningGate
from src.application.schemas.user_careers import UserCareersSchema
from src.usecase.user_careers.schemas import GetUpdateUserCareersSchema
from src.infra.postgres.tables import UserCareersModel
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class UpdateUserCareersUsecase(Usecase[GetUpdateUserCareersSchema, UserCareersSchema]):
    session: AsyncSession
    update_usercareers: UpdateReturningGate[UserCareersModel, UserCareersModel, UUID, UserCareersSchema]
    async def __call__(self, data: GetUpdateUserCareersSchema) -> None:
        async with self.session.begin():
            return await self.update_usercareers(data)