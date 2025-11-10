from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.usecase.cards.schemas import GetUpdateCardsSchema
from src.usecase.cards.update import UpdateCardUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.put('', status_code=status.HTTP_200_OK)
async def update_card(
    usecase: FromDishka[UpdateCardUsecase],
    card: GetUpdateCardsSchema) -> None:
    return await usecase(card)