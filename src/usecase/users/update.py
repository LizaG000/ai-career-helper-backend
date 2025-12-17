from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import UpdateReturningGate
from src.application.schemas.users import UserSchemas, UpdateUserSchema
from src.usecase.users.schemas import GetUpdateUserSchema
from src.infra.postgres.tables import UserModel
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class UpdateUserNameUsecase(Usecase[GetUpdateUserSchema, UserSchemas]):
    session: AsyncSession
    update_user_name: UpdateReturningGate[UserModel, UpdateUserSchema, UUID, UserSchemas]
    async def __call__(self, data: GetUpdateUserSchema) -> UserSchemas:
        async with self.session.begin():
            return await self.update_user_name(entity_id=data.id, entity=data.user)