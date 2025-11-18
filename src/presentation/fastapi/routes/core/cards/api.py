from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.cards import CardSchema
from src.usecase.cards.delete import DeleteCardUsecase
from src.usecase.cards.schemas import GetUpdateCardsSchema
from src.usecase.cards.update import UpdateCardUsecase
from src.usecase.cards.get_all import GetAllCardsUsecase
from src.usecase.cards.schemas import PaginationSchema, CardsSchema
from uuid import UUID

ROUTER = APIRouter(route_class=DishkaRoute, )

@ROUTER.delete('', status_code=status.HTTP_200_OK)
async def delete_cards(
    usecase: FromDishka[DeleteCardUsecase],
    id: UUID) -> CardSchema:
    return await usecase(id)

@ROUTER.get('', status_code=status.HTTP_200_OK)
async def get_cards(
    usecase: FromDishka[GetAllCardsUsecase],
    limit: int,
    offset:int) -> list[CardsSchema]:
    return await usecase(PaginationSchema(limit=limit, offset=offset))

@ROUTER.put('', status_code=status.HTTP_200_OK)
async def update_card(
    usecase: FromDishka[UpdateCardUsecase],
    card: GetUpdateCardsSchema) -> CardSchema:
    return await usecase(card)
