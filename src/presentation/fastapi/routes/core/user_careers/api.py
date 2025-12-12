from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.application.schemas.user_careers import CreateUserCareersSchema, UserCareersSchema
from src.usecase.user_careers.create import CreateUserCareerUsecase

ROUTER = APIRouter(route_class=DishkaRoute)


@ROUTER.post("", status_code=status.HTTP_200_OK)
async def create_users_career(
    usecase: FromDishka[CreateUserCareerUsecase], user: CreateUserCareersSchema
) -> UserCareersSchema:
    return await usecase(user)
