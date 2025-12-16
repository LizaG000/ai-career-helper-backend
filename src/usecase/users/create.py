from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.application.schemas.users import CreateUserSchema, UserSchema
from src.infra.postgres.tables import UserModel
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserUsecase(Usecase[CreateUserSchema, UserSchema]):
    session: AsyncSession
    create_user: CreateReturningGate[UserModel, CreateUserSchema, UserSchema]

    async def __call__(self, data: CreateUserSchema) -> None:
        async with self.session.begin():
            return await self.create_user(data)
