from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.schemas.cards import CardSchema, UpdateCardSchema
from src.infra.postgres.gateways.base import UpdateReturningGate
from src.infra.postgres.tables import CardsModel
from src.usecase.base import Usecase
from src.usecase.cards.schemas import GetUpdateCardsSchema


@dataclass(slots=True, frozen=True, kw_only=True)
# karoche tut ne UpdateCardSchema tut is usecase/cards/schemas, ne None, a CardsShema
class UpdateCardUsecase(Usecase[GetUpdateCardsSchema, CardSchema]):
    session: AsyncSession
    update_card: UpdateReturningGate[CardsModel, UpdateCardSchema, UUID, CardSchema]

    # isprav None na tip vozvrachenia
    async def __call__(self, data: GetUpdateCardsSchema) -> CardSchema:
        # vozvrashay rabotu usecasa
        async with self.session.begin():
            return await self.update_card(entity_id=data.id, entity=data.card)
