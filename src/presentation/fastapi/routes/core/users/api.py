from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.users import CreateUserSchema
from src.usecase.users.create import CreateUserUsecase
ROUTER = APIRouter(route_class=DishkaRoute)
from fastapi import APIRouter, Depends
from typing import Any
from src.application.schemas.users import UserCreate
from src.application.schemas.user_careers import UserCareerCreate
from src.usecase.user.create_user_profile import CreateUserProfileUseCase
from src.main.provider import get_create_user_profile_usecase

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/profile", response_model=dict[str, Any])
async def create_user_profile(
    user_data: UserCreate,
    career_data: UserCareerCreate,
    usecase: CreateUserProfileUseCase = Depends(get_create_user_profile_usecase)
) -> dict[str, Any]:
    user, user_career = await usecase.execute(user_data, career_data)
    
    return {
        "user": user,
        "user_career": user_career,
        "message": "User profile created successfully"
    }

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_users(
    usecase: FromDishka[CreateUserUsecase],
    user: CreateUserSchema) -> None:
    await usecase(user)
