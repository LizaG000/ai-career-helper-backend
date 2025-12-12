from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Select, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.dml import ReturningInsert, ReturningUpdate

from src.application.errors import (
    DatabaseCreateError,
    DatabaseDeleteError,
    DatabaseUpdateError,
    NotFoundError,
)
from src.infra.postgres.tables import BaseDBModel

TAppliable = Select | ReturningInsert | ReturningUpdate

TTable = TypeVar("TTable", bound=BaseDBModel)
TEntity = TypeVar("TEntity", bound=BaseModel)
TCreate = TypeVar("TCreate", bound=BaseModel)
TUpdate = TypeVar("TUpdate", bound=BaseModel)
TEntityId = TypeVar("TEntityId", bound=UUID)


@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession


@dataclass(slots=True, kw_only=True)
class GetAllGate(Generic[TTable, TEntity], PostgresGateway):
    table: type[TTable]
    schema_type: type[TEntity]

    async def __call__(self) -> list[TEntity] | list[None]:
        stmt = Select(*self.table.group_by_fields())
        results = (await self.session.execute(stmt)).mappings().fetchall()
        if results == []:
            return results
        return [self.schema_type.model_validate(result) for result in results]


@dataclass(slots=True, kw_only=True)
class GetAllByIdUserGate(Generic[TTable, TEntity, TEntityId], PostgresGateway):
    table: type[TTable]
    schema_type: type[TEntity]
    entity_id: type[TEntityId]

    async def __call__(self, id_user=TEntityId) -> list[TEntity] | list[None]:
        stmt = Select(*self.table.group_by_fields()).where(self.table.id_user == id_user)
        results = (await self.session.execute(stmt)).mappings().fetchall()
        if results == []:
            return results
        return [self.schema_type.model_validate(result) for result in results]


@dataclass(slots=True, kw_only=True)
class GetByIdGate(Generic[TTable, TEntityId, TEntity], PostgresGateway):
    table: type[TTable]
    schema_type: type[TEntity]
    entity_id: type[TEntityId]

    async def __call__(self, id=TEntityId) -> TEntity:
        stmt = select(*self.table.group_by_fields()).where(self.table.id == id)
        result = (await self.session.execute(stmt)).mappings().fetchone()
        print(result)
        if result is None:
            raise NotFoundError(self.table)
        return self.schema_type.model_validate(result)


@dataclass(slots=True, kw_only=True)
class CreateGate(Generic[TTable, TCreate], PostgresGateway):
    table: type[TTable]
    create_schema_type: type[TCreate]

    async def __call__(self, entity: TCreate) -> None:
        stmt = insert(self.table).values(**entity.model_dump())
        try:
            await self.session.execute(stmt)
        except:
            raise DatabaseCreateError(self.table)


@dataclass(slots=True, kw_only=True)
class CreateReturningGate(Generic[TTable, TCreate, TEntity], PostgresGateway):
    table: type[TTable]
    create_schema_type: type[TCreate]
    schema_type: type[TEntity]

    async def __call__(self, entity: TCreate) -> TEntity:
        stmt = insert(self.table).values(**entity.model_dump()).returning(self.table)
        try:
            result = (await self.session.execute(stmt)).scalar_one().__dict__
            return self.schema_type.model_validate(result)
        except:
            raise DatabaseCreateError(self.table)


@dataclass(slots=True, kw_only=True)
class UpdateGate(Generic[TTable, TUpdate, TEntityId], PostgresGateway):
    table: type[TTable]
    update_schema_type: type[TUpdate]
    entity_id: type[TEntityId]

    async def __call__(self, entity: TCreate, entity_id: TEntityId) -> None:
        stmt = update(self.table).where(self.table.id == entity_id).values(**entity.model_dump())
        try:
            await self.session.execute(stmt)
        except:
            raise DatabaseUpdateError(self.table)


@dataclass(slots=True, kw_only=True)
class UpdateReturningGate(Generic[TTable, TUpdate, TEntityId, TEntity], PostgresGateway):
    table: type[TTable]
    update_schema_type: type[TUpdate]
    entity_id: type[TEntityId]
    schema_type: type[TEntity]

    async def __call__(self, entity_id: TEntityId, entity: TUpdate) -> TEntity:
        stmt = (
            update(self.table)
            .where(self.table.id == entity_id)
            .values(**entity.model_dump(exclude_none=True))
            .returning(self.table)
        )
        try:
            result = (await self.session.execute(stmt)).scalar_one().__dict__
            return self.schema_type.model_validate(result)
        except:
            raise DatabaseUpdateError(self.table)


@dataclass(slots=True, kw_only=True)
class DeleteGate(Generic[TTable, TEntityId], PostgresGateway):
    table: type[TTable]
    entity_id: type[TEntityId]

    async def __call__(self, entity_id: TEntityId) -> None:
        stmt = delete(self.table).where(self.table.id == entity_id)
        try:
            await self.session.execute(stmt)
        except:
            raise DatabaseDeleteError(self.table)


@dataclass(slots=True, kw_only=True)
class DeleteReturningGate(Generic[TTable, TEntityId, TEntity], PostgresGateway):
    table: type[TTable]
    entity_id: type[TEntityId]
    schema_type: type[TEntity]

    async def __call__(self, entity_id: TEntityId) -> TEntity:
        stmt = delete(self.table).where(self.table.id == entity_id).returning(self.table)
        try:
            result = (await self.session.execute(stmt)).scalar_one().__dict__
            return self.schema_type.model_validate(result)
        except:
            raise DatabaseDeleteError(self.table)
