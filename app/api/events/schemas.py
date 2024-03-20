from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class UpdateEventStatusEnum(str, Enum):
    WIN = "WIN"
    LOSE = "LOSE"


class CreateEvent(BaseModel):
    title: str = Field(min_length=1, max_length=256)


class GetEvent(BaseModel):
    id: str  # noqa
    title: str

    created_at: datetime


class UpdateEventStatus(BaseModel):
    status: UpdateEventStatusEnum
