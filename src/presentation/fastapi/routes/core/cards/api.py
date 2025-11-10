from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.cards import CardSchema
from src.application.schemas.users import CreateUserSchema
from src.usecase.users.create import CreateUserUsecase
from src.usecase.cards.delete import DeleteCardUsecase
from uuid import UUID

ROUTER = APIRouter(route_class=DishkaRoute, )

@ROUTER.delete('', status_code=status.HTTP_200_OK)
async def delete_cards(
    usecase: FromDishka[DeleteCardUsecase],
    id: UUID) -> CardSchema:
    return await usecase(id)
