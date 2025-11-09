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

class UserCareersModel(BaseDBModel):
    __tablename__ = 'user_careers'
    id: Mapped[uuid_pk]
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False,
    )
    specialization_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False
    )
    experience_level: Mapped[enumerate] = mapped_column(
        enum,
        nullable=False
    )
    skills: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    career_goal: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    '''timestamp'''

class UserResumeModel(BaseDBModel):
    __tablename__ = 'user_resume'
    id: Mapped[uuid_pk]
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    work_experience: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )
    skills: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    recomendations: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class SpecializationsModel(BaseDBModel):
    __tablename__ = 'specializations'
    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    '''timestamp'''

class RoadmapsModel(BaseDBModel):
    __tablename__ = 'roadmaps'
    id: Mapped[uuid_pk]
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    '''timestamp
    start_date: Mapped[start_date]
    estmated_end_date: Mapped[estmated_end_date]
    DATE'''

class RoadmapStatusModel(BaseDBModel):
    __tablename__ = 'roadmap_status'
    id: Mapped[uuid_pk]
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    '''timestamp'''

class RoadMapStepsModel(BaseDBModel):
    __tablename__ = 'roadmapsteps'
    id: Mapped[uuid_pk]
    roadmap_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        nullable=False,
    )
    step_number: Mapped[int] = mapped_column(
        int,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    materials: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    deadline: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    '''timestamp'''

    


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