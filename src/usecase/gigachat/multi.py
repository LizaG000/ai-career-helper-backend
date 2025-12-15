from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.gigachat.schemas import AgentState
from dataclasses import dataclass
from src.usecase.message.schemas import RequestMessageSchema
from src.infra.gigachat.agents.orchestrator import OrchestratorAgent

@dataclass(slots=True, frozen=True, kw_only=True)
class MultyUsecase(Usecase[RequestMessageSchema, str]):
    session: AsyncSession

    orchestrator: OrchestratorAgent

    async def __call__(self, data: RequestMessageSchema) -> str:


        async with self.session.begin():
            self.orchestrator.




