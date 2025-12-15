from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.application.schemas.auth import AuthSchema
from src.infra.postgres.gateways.base import CreateReturningGate
from src.application.schemas.chats import CreateChatSchema, ChatSchemas
from src.infra.postgres.tables import ChatModel
from dataclasses import dataclass


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateChatUsecase(Usecase[CreateChatSchema, None]):
    session: AsyncSession
    auth: AuthSchema
    create_chat: CreateReturningGate[ChatModel,CreateChatSchema, ChatSchemas]

    async def __call__(self, data: CreateChatSchema) -> ChatSchemas:
        async with self.session.begin():
            return await self.create_chat(data)
