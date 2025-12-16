from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from src.usecase.base import Usecase
from src.application.schemas.auth import AuthSchema
from src.infra.postgres.gateways.base import CreateGate, CreateReturningGate, GetByIdGate
from src.application.schemas.chats import CreateChatSchema, ChatSchemas
from src.infra.postgres.tables import ChatModel, MessageModel
from src.application.schemas.messages import CreateMessageSchema
from  src.usecase.chats.schemas import GetChatMessaesSchema
from src.usecase.users.create import CreateUserUsecase
from src.application.schemas.users import CreateUserSchema
from src.infra.postgres.gateways.chats import GetChatGate
from dataclasses import dataclass


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateChatUsecase(Usecase[CreateChatSchema, GetChatMessaesSchema]):
    session: AsyncSession
    auth: AuthSchema
    create_chat: CreateReturningGate[ChatModel,CreateChatSchema, ChatSchemas]
    create_message: CreateGate[MessageModel, CreateMessageSchema]
    get_chat: GetChatGate
    create_user: CreateUserUsecase

    async def __call__(self, data: CreateChatSchema) -> GetChatMessaesSchema:
        async with self.session.begin():
            await self.create_user(CreateUserSchema(id=self.auth.id))
            chat = await self.create_chat(data)
            await self.create_message(CreateMessageSchema(
                chat_id=chat.id,
                text="Привет! Чем я могу помочь?)",
                sender_type_id="chat"
            ))
            return await self.get_chat(chat_id=chat.id)
