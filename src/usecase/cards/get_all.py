from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.postgres.gateways.cards import GetCardsGate
from src.usecase.base import Usecase
from src.usecase.cards.schemas import PaginationSchema, ResponseCardsSchema


@dataclass(slots=True, frozen=True, kw_only=True)
class GetAllCardsUsecase(Usecase[PaginationSchema, ResponseCardsSchema]):
    session: AsyncSession
    get_cards: GetCardsGate

    async def __call__(self, data: PaginationSchema) -> ResponseCardsSchema:
        async with self.session.begin():
            return await self.get_cards(limit=data.limit, offset=data.offset)
