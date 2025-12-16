from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.chats import CreateChatSchema, ChatSchemas
from src.usecase.chats.create import CreateChatUsecase
from src.application.schemas.common import RequestPaginationByIDSchema, ResponsePaginationSchema, RequestPaginationSchema
from src.usecase.chats.get import GetChatUsecase
from src.usecase.chats.schemas import GetChatMessaesSchema
from src.usecase.chats.get_all import GetAllChatUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=GetChatMessaesSchema)
async def create_chat(
    usecase: FromDishka[CreateChatUsecase],
    data: CreateChatSchema) -> GetChatMessaesSchema:
    return await usecase(data)

@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=ResponsePaginationSchema[GetChatMessaesSchema])
async def get_chat(
    usecase: FromDishka[GetChatUsecase],
    data: RequestPaginationByIDSchema) -> ResponsePaginationSchema[GetChatMessaesSchema]:
    return await usecase(data)

@ROUTER.get('/all', status_code=status.HTTP_200_OK, response_model=ResponsePaginationSchema[ChatSchemas])
async def get_all_chat(
    usecase: FromDishka[GetAllChatUsecase],
    data: RequestPaginationSchema) -> ResponsePaginationSchema[ChatSchemas]:
    return await usecase(data)
