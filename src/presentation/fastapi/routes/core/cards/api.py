from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from loguru import logger
from src.application.schemas.cards import CardSchema
from src.application.schemas.tasks import CardTaskRequest, CardTaskResponse
from src.infra.taskiq.tasks import enqueue_card_task
from src.usecase.cards.delete import DeleteCardUsecase
from src.usecase.cards.schemas import GetUpdateCardsSchema
from src.usecase.cards.update import UpdateCardUsecase
from src.usecase.cards.generate import GenerateCardsUsecase

from src.usecase.cards.get_all import GetAllCardsUsecase
from src.usecase.cards.schemas import PaginationSchema, ResponseCardsSchema
from src.usecase.cards.create import CreateCardsUsecase
from src.usecase.cards.schemas import CreateManyCardsSchema
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
    offset:int) -> ResponseCardsSchema:
    return await usecase(PaginationSchema(limit=limit, offset=offset))

@ROUTER.put('', status_code=status.HTTP_200_OK)
async def update_card(
    usecase: FromDishka[UpdateCardUsecase],
    card: GetUpdateCardsSchema) -> CardSchema:
    return await usecase(card)

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_cards(
    usecase: FromDishka[CreateCardsUsecase],
    cards: CreateManyCardsSchema
) -> list[CardSchema]:
    return await usecase(cards.cards)

@ROUTER.post('/tasks', status_code=status.HTTP_202_ACCEPTED)
async def create_card_task(
    request: CardTaskRequest,
) -> CardTaskResponse:
    try:
        return await enqueue_card_task(request)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to enqueue card task: {}", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to enqueue task",
        )

@ROUTER.post('/generate', status_code=status.HTTP_200_OK)
async def generate_cards(
    usecase: FromDishka[GenerateCardsUsecase],
) -> list[CardSchema]:
    return await usecase()
