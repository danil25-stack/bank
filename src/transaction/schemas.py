from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List


class TransactionCreate(BaseModel):
    account_id: int
    transaction_type: str  # debit / credit
    booking_date: date
    value_date: date
    amount: float
    currency: str
    creditor_name: str | None = None
    debtor_name: str | None = None
    remittance_information: str | None = None


class TransactionOut(TransactionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedTransaction(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[TransactionOut]
