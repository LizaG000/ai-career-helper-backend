from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.users import CreateUserSchema, UserSchemas
from src.usecase.users.schemas import GetUpdateUserSchema
from src.usecase.users.create import CreateUserUsecase
from src.usecase.users.update import UpdateUserNameUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_users(
    usecase: FromDishka[CreateUserUsecase],
    user: CreateUserSchema) -> None:
    await usecase(user)

@ROUTER.put('/{user_id}', status_code=status.HTTP_200_OK)
async def update_user(
    usecase: FromDishka[UpdateUserNameUsecase],
    data: GetUpdateUserSchema
) -> UserSchemas:

    return await usecase(data)