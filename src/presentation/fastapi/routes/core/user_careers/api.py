from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.user_careers import CreateUserCareersSchema, UserCareersSchema
from src.usecase.user_careers.create import CreateUserCareerUsecase
from src.usecase.user_careers.schemas import GetUpdateUserCareersSchema
from src.usecase.user_careers.update import UpdateUserCareersUsecase

ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_users_career(
    usecase: FromDishka[CreateUserCareerUsecase],
    user: CreateUserCareersSchema) -> UserCareersSchema:
    return await usecase(user)

@ROUTER.put('', status_code=status.HTTP_200_OK)
async def update_user_careers(
    usecase: FromDishka[UpdateUserCareersUsecase],
    usercareer: GetUpdateUserCareersSchema) -> UserCareersSchema:
    return await usecase(usercareer)
