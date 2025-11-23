from pydantic import BaseModel
from datetime import date


class BalanceCreate(BaseModel):
    account_id: int
    balance_type: str
    amount: float
    currency: str
    reference_date: date


class BalanceOut(BalanceCreate):
    id: int

    class Config:
        orm_mode = True
