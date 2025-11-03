import uuid
from datetime import datetime
from sqlalchemy import UUID
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from typing import Annotated, Optional
import enum

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

class ExperienceLevel(enum.Enum):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    LEAD = "lead"

class StepStatus(enum.Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

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
    age: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )
    phone: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    password: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    resumes: Mapped[list['UserResumeModel']] = relationship(back_populates="user")
    careers: Mapped[list['UserCareerModel']] = relationship(back_populates="user")
    roadmap_steps: Mapped[list['RoadmapStepModel']] = relationship(back_populates="user")
    learning_roadmaps: Mapped[list['LearningRoadmapModel']] = relationship(back_populates="user")


class UserResumeModel(BaseDBModel):
    __tablename__ = 'user_resume'

    id: Mapped[uuid_pk]
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('db_schema.users.id'),
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    work_experience: Mapped[Optional[str]] = mapped_column(Text)
    skills: Mapped[Optional[str]] = mapped_column(Text)
    recommendations: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped['UserModel'] = relationship(back_populates="resumes")


class SpecializationModel(BaseDBModel):
    __tablename__ = 'specializations'

    id: Mapped[uuid_pk]
    name: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user_careers: Mapped[list['UserCareerModel']] = relationship(back_populates="specialization")


class UserCareerModel(BaseDBModel):
    __tablename__ = 'user_careers'

    id: Mapped[uuid_pk]
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('db_schema.users.id'),
        nullable=False
    )
    specialization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('db_schema.specializations.id'),
        nullable=False,
        unique=True
    )
    experience_level: Mapped[ExperienceLevel] = mapped_column(
        Enum(ExperienceLevel),
        nullable=False
    )
    skills: Mapped[Optional[str]] = mapped_column(Text)
    career_goals: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped['UserModel'] = relationship(back_populates="careers")
    specialization: Mapped['SpecializationModel'] = relationship(back_populates="user_careers")


class LearningRoadmapModel(BaseDBModel):
    __tablename__ = 'learning_roadmap'

    id: Mapped[uuid_pk]
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('db_schema.users.id'),
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[StepStatus] = mapped_column(
        Enum(StepStatus),
        default=StepStatus.DRAFT
    )
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    estimated_end_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    actual_end_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped['UserModel'] = relationship(back_populates="learning_roadmaps")
    roadmap_steps: Mapped[list['RoadmapStepModel']] = relationship(back_populates="roadmap")


class RoadmapStepModel(BaseDBModel):
    __tablename__ = 'roadmap_steps'

    id: Mapped[uuid_pk]
    roadmap_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('db_schema.learning_roadmap.id'),
        nullable=False
    )
    step_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(Text)
    materials: Mapped[Optional[str]] = mapped_column(Text)
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime)
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    roadmap: Mapped['LearningRoadmapModel'] = relationship(back_populates="roadmap_steps")


class RoadmapStatusModel(BaseDBModel):
    __tablename__ = 'roadmap_status'

    id: Mapped[uuid_pk]
    status: Mapped[Optional[str]] = mapped_column(String(255))
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
