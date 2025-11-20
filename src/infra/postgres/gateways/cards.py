from src.infra.postgres.gateways.base import PostgresGateway
from src.infra.postgres.tables import CardsModel, InformationsModel
from dataclasses import dataclass
from sqlalchemy import select, func, literal
from sqlalchemy import func, over
from  src.usecase.cards.schemas import CardsSchema
from loguru import logger

@dataclass(slots=True, kw_only=True)
class GetCardsGate(PostgresGateway):
    async  def __call__(self, limit: int, offset: int) -> list[CardsSchema]:
        numbered_cards = (
            select(
                CardsModel.id,
                CardsModel.title,
                CardsModel.description,
                CardsModel.created_at,
                CardsModel.information_id,
                InformationsModel.created_at.label('info_created_at'),
                func.row_number().over(
                    order_by=(
                        InformationsModel.created_at.desc(),
                        CardsModel.created_at
                    )
                ).label('global_card_num')
            )
            .join(InformationsModel, InformationsModel.id == CardsModel.information_id)
            .subquery()
        )

        limited_cards = (
            select(
                numbered_cards.c.id,
                numbered_cards.c.title,
                numbered_cards.c.description,
                numbered_cards.c.created_at,
                numbered_cards.c.information_id,
                numbered_cards.c.info_created_at
            )
            .where(numbered_cards.c.global_card_num <= limit + offset * (limit-1))
            .where(numbered_cards.c.global_card_num > offset * limit)
            .subquery()
        )

        cards_agg = (
            select(
                limited_cards.c.information_id,
                func.json_agg(
                    func.json_build_object(
                        'id', limited_cards.c.id,
                        'title', limited_cards.c.title,
                        'description', limited_cards.c.description,
                        'created_at', limited_cards.c.created_at
                    )
                ).label('cards')
            )
            .group_by(limited_cards.c.information_id)
            .subquery()
        )

        stmt = (
            select(
                InformationsModel.id,
                InformationsModel.title,
                InformationsModel.created_at,
                cards_agg.c.cards
            )
            .join(cards_agg, InformationsModel.id == cards_agg.c.information_id)
            .order_by(InformationsModel.created_at.desc())  # информация по убыванию
        )

        results = (await self.session.execute(stmt)).mappings().fetchall()
        logger.info(results)
        if results == []:
            return results
        return [CardsSchema.model_validate(result) for result in results]