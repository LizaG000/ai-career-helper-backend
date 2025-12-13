from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from loguru import logger
from pydantic import BaseModel

from src.application.schemas.tasks import (
    CardTaskRequest,
    CardTaskResponse,
    CardUsecaseName,
    DeleteCardTaskPayload,
)
from src.infra.taskiq.broker import broker
from src.main.container import container
from src.usecase.cards.create import CreateCardsUsecase
from src.usecase.cards.delete import DeleteCardUsecase
from src.usecase.cards.generate import GenerateCardsUsecase
from src.usecase.cards.get_all import GetAllCardsUsecase
from src.usecase.cards.schemas import CreateManyCardsSchema, GetUpdateCardsSchema, PaginationSchema
from src.usecase.cards.update import UpdateCardUsecase


@dataclass(frozen=True)
class CardTaskDescriptor:
    usecase_cls: type
    payload_schema: type[BaseModel] | None
    argument_builder: Callable[[BaseModel | None], Any]


CARD_TASKS: dict[CardUsecaseName, CardTaskDescriptor] = {
    CardUsecaseName.CREATE: CardTaskDescriptor(
        usecase_cls=CreateCardsUsecase,
        payload_schema=CreateManyCardsSchema,
        argument_builder=lambda payload: payload.cards if payload else [],
    ),
    CardUsecaseName.UPDATE: CardTaskDescriptor(
        usecase_cls=UpdateCardUsecase,
        payload_schema=GetUpdateCardsSchema,
        argument_builder=lambda payload: payload,
    ),
    CardUsecaseName.DELETE: CardTaskDescriptor(
        usecase_cls=DeleteCardUsecase,
        payload_schema=DeleteCardTaskPayload,
        argument_builder=lambda payload: payload.id if payload else None,
    ),
    CardUsecaseName.GENERATE: CardTaskDescriptor(
        usecase_cls=GenerateCardsUsecase,
        payload_schema=None,
        argument_builder=lambda _payload: None,
    ),
    CardUsecaseName.GET_ALL: CardTaskDescriptor(
        usecase_cls=GetAllCardsUsecase,
        payload_schema=PaginationSchema,
        argument_builder=lambda payload: payload,
    ),
}


def _validate_payload(usecase_name: CardUsecaseName, payload: dict | None) -> dict | None:
    descriptor = CARD_TASKS[usecase_name]
    if descriptor.payload_schema is None:
        return None

    if payload is None:
        raise ValueError(f"Payload is required for usecase '{usecase_name.value}'.")

    parsed = descriptor.payload_schema.model_validate(payload)
    return parsed.model_dump()


async def enqueue_card_task(request: CardTaskRequest) -> CardTaskResponse:
    validated_payload = _validate_payload(request.usecase, request.payload)

    task_message = await execute_card_usecase.kiq(
        usecase=request.usecase.value,
        payload=validated_payload,
    )
    task_id = getattr(task_message, "task_id", None) or getattr(task_message, "message_id", None)
    if task_id is None:
        logger.warning("Task was enqueued but task id is not available in response.")
        task_id = ""
    return CardTaskResponse(
        task_id=str(task_id),
        usecase=request.usecase,
        payload=validated_payload,
    )


@broker.task
async def execute_card_usecase(usecase: str, payload: dict | None = None) -> Any:
    usecase_name = CardUsecaseName(usecase)
    descriptor = CARD_TASKS[usecase_name]

    parsed_payload: BaseModel | None = None
    if descriptor.payload_schema is not None:
        parsed_payload = descriptor.payload_schema.model_validate(payload or {})

    argument = descriptor.argument_builder(parsed_payload)

    async with container() as scope:
        usecase_instance = await scope.get(descriptor.usecase_cls)
        result = await usecase_instance(argument)

    return _serialize_result(result)


def _serialize_result(result: Any) -> Any:
    if isinstance(result, BaseModel):
        return result.model_dump()
    if isinstance(result, list):
        return [_serialize_result(item) for item in result]
    return result
