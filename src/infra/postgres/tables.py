import uuid
from datetime import datetime
from sqlalchemy import UUID
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from typing import Annotated

uuid_pk = Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )]

created_at = Annotated[datetime, mapped_column(
    DateTime(timezone=True),
    default=func.now(), 
    nullable=False,

)]
updated_at = Annotated[datetime, mapped_column(
    DateTime(timezone=True),
    default=func.now(), 
    nullable=False,

)]

class BaseDBModel(DeclarativeBase):
    __tablename__: str
    __table_args__: dict[str, str] | tuple = {'schema': 'db_schema'}

    @classmethod
    def group_by_fields(cls, exclude: list[str] | None = None) -> list:
        payload = []
        if not exclude:
            exclude = []

        for column in cls.__table__.columns:
            if column.key in exclude:
                continue

            payload.append(column)

        return payload

class UserModel(BaseDBModel):
    __tablename__ = 'users'
    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    corporate_account_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )
    
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class InformationsModel(BaseDBModel):
    __tablename__ = 'informations'
    id: Mapped[uuid_pk]
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class CardsModel(BaseDBModel):
    __tablename__ = 'informations'
    id: Mapped[uuid_pk]
    information_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('db_schema.informations.id'),
        nullable=False,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]