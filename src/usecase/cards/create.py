from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.application.schemas.cards import CardSchema, CreateCardSchema
from src.infra.postgres.tables import CardsModel
from src.infra.postgres.gateways.base import CreateReturningGate

@dataclass(slots=True, kw_only=True)
class CreateCardsUsecase:
    session: AsyncSession
    create_card: CreateReturningGate[CardsModel, CreateCardSchema, CardSchema]

    async def __call__(self, cards: List[CreateCardSchema]) -> List[CardSchema]:
        results: List[CardSchema] = []
        async with self.session.begin():
            for card in cards:
                created = await self.create_card(card)
                results.append(created)
        return results
