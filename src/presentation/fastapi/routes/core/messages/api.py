from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.usecase.message.schemas import RequestMessageSchema
from src.usecase.message.create import MessengerUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_message(
    usecase: FromDishka[MessengerUsecase],
    user: RequestMessageSchema) -> None:
    await usecase(user)
