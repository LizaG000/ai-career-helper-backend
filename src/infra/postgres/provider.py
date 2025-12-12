from collections.abc import AsyncIterator
from typing import TypeVar

from dishka import Provider, Scope, provide, provide_all
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from src.config import DatabaseConfig
from src.infra.postgres.gateways.base import (
    CreateGate,
    CreateReturningGate,
    DeleteGate,
    DeleteReturningGate,
    GetAllByIdUserGate,
    GetAllGate,
    GetByIdGate,
    UpdateGate,
    UpdateReturningGate,
)
from src.infra.postgres.gateways.cards import GetCardsGate

TTable = TypeVar("TTable")
TEntity = TypeVar("TEntity")
TEntityId = TypeVar("TEntityId")
TCreate = TypeVar("TCreate")
TUpdate = TypeVar("TUpdate")


class PostgresProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def _get_engine(self, config: DatabaseConfig) -> AsyncIterator[AsyncEngine]:
        engine: AsyncEngine | None = None
        try:
            if engine is None:
                engine = create_async_engine(config.dsn)
            yield engine
        except ConnectionRefusedError as e:
            logger.error("Error connecting to database", e)
        finally:
            if engine is not None:
                await engine.dispose()

    @provide
    async def _get_session_maker(self, engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
        async with AsyncSession(bind=engine) as session:
            yield session

    @provide
    async def _get_all_gate(
        self,
        table: type[TTable],
        schema_type: type[TEntity],
        session: AsyncSession,
    ) -> GetAllGate[TTable, TEntity]:
        return GetAllGate(
            session=session,
            table=table,
            schema_type=schema_type,
        )

    @provide
    async def _get_all_by_id_user_gate(
        self,
        table: type[TTable],
        schema_type: type[TEntity],
        entity_id: type[TEntityId],
        session: AsyncSession,
    ) -> GetAllByIdUserGate[TTable, TEntity, TEntityId]:
        return GetAllByIdUserGate(
            session=session,
            table=table,
            schema_type=schema_type,
            entity_id=entity_id,
        )

    @provide
    async def _get_by_id_gate(
        self,
        table: type[TTable],
        entity_id: type[TEntityId],
        schema_type: type[TEntity],
        session: AsyncSession,
    ) -> GetByIdGate[TTable, TEntityId, TEntity]:
        return GetByIdGate(
            session=session,
            table=table,
            entity_id=entity_id,
            schema_type=schema_type,
        )

    @provide
    async def _create_gate(
        self,
        table: type[TTable],
        create_schema_type: type[TCreate],
        session: AsyncSession,
    ) -> CreateGate[TTable, TCreate]:
        return CreateGate(
            session=session,
            table=table,
            create_schema_type=create_schema_type,
        )

    @provide
    async def _create_returning_gate(
        self,
        table: type[TTable],
        create_schema_type: type[TCreate],
        schema_type: type[TEntity],
        session: AsyncSession,
    ) -> CreateReturningGate[TTable, TCreate, TEntity]:
        return CreateReturningGate(
            session=session,
            table=table,
            create_schema_type=create_schema_type,
            schema_type=schema_type,
        )

    @provide
    async def _update_gate(
        self,
        table: type[TTable],
        update_schema_type: type[TUpdate],
        entity_id: type[TEntityId],
        session: AsyncSession,
    ) -> UpdateGate[TTable, TUpdate, TEntityId]:
        return UpdateGate(
            session=session,
            table=table,
            update_schema_type=update_schema_type,
            entity_id=entity_id,
        )

    @provide
    async def _update_returning_gate(
        self,
        table: type[TTable],
        update_schema_type: type[TUpdate],
        entity_id: type[TEntityId],
        schema_type: type[TEntity],
        session: AsyncSession,
    ) -> UpdateReturningGate[TTable, TUpdate, TEntityId, TEntity]:
        return UpdateReturningGate(
            session=session,
            table=table,
            update_schema_type=update_schema_type,
            entity_id=entity_id,
            schema_type=schema_type,
        )

    @provide
    async def _delete_gate(
        self,
        table: type[TTable],
        entity_id: type[TEntityId],
        session: AsyncSession,
    ) -> DeleteGate[TTable, TEntityId]:
        return DeleteGate(
            session=session,
            table=table,
            entity_id=entity_id,
        )

    @provide
    async def _delete_returning_gate(
        self,
        table: type[TTable],
        entity_id: type[TEntityId],
        schema_type: type[TEntity],
        session: AsyncSession,
    ) -> DeleteReturningGate[TTable, TEntityId, TEntity]:
        return DeleteReturningGate(
            session=session,
            table=table,
            entity_id=entity_id,
            schema_type=schema_type,
        )

    _get_gateways_ = provide_all(
        GetCardsGate,
    )
