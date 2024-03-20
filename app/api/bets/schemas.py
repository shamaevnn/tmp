from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class GetBet(BaseModel):
    id: str  # noqa
    status: str
    created_at: datetime


class CreateBet(BaseModel):
    amount: Decimal = Field(gt=0.01)
    event_id: str


class CreateBetResponse(BaseModel):
    id: str  # noqa
