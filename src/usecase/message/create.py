from multiprocessing.connection import answer_challenge
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.infra.postgres.tables import MessagesModel
from src.application.schemas.messages import MessageSchemas, CreateMessageSchema
from src.application.schemas.auth import AuthSchema
from src.usecase.message.schemas import RequestMessageSchema

from src.infra.gigachat.agents.orchestrator import OrchestratorAgent

@dataclass(slots=True, frozen=True, kw_only=True)
class MessengerUsecase(Usecase[RequestMessageSchema, MessageSchemas]):
    session: AsyncSession
    auth: AuthSchema
    create_message: CreateReturningGate[MessagesModel, CreateMessageSchema, MessageSchemas]
    orchestrator: OrchestratorAgent

    async def __call__(self, data: RequestMessageSchema) -> MessageSchemas:
        async with self.session.begin():
            await self.create_message(CreateMessageSchema(
                chat_id=data.chat_id,
                text=data.text,
                sender_type_id=UUID("c2a9e7f1-5b83-4d2c-91a6-8f3b0c4d5e6f")
            ))
            answer = await self.orchestrator(data=data)

            return await self.create_message(CreateMessageSchema(
                chat_id=data.chat_id,
                text=answer,
                sender_type_id=UUID("9d8a2b7c-4e1f-4a3d-85c9-0b6a1e3f8d2c")
            ))
