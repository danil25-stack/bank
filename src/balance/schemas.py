from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List


class BalanceCreate(BaseModel):
    account_id: int
    balance_type: str
    amount: float
    currency: str
    reference_date: date


class BalanceOut(BalanceCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedBalance(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[BalanceOut]
