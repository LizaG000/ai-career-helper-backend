from src.usecase.base import Usecase
from uuid import UUID
from src.infra.postgres.gateways.base import CreateGate, GetByIdGate
from src.application.schemas.users import CreateUserSchema, UserSchemas
from src.infra.postgres.tables import UserModel
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserUsecase(Usecase[CreateUserSchema, None]):
    create_user: CreateGate[UserModel, CreateUserSchema]
    get_user: GetByIdGate[UserModel, UUID, UserSchemas]
    
    async def __call__(self, data: CreateUserSchema) -> None:
        try:
            await self.get_user(data.id)
        except:
            await self.create_user(data)
