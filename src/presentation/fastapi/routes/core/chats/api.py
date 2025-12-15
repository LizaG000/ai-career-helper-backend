from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.chats import CreateChatSchema, ChatSchemas
from src.usecase.chats.create import CreateChatUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_chat(
    usecase: FromDishka[CreateChatUsecase],
    data: CreateChatSchema) -> ChatSchemas:
    return await usecase(data)
