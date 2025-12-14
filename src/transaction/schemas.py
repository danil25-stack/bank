from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List
from src.transaction.models import SourceType


class TransactionCreate(BaseModel):
    account_id: int
    transaction_type: str
    booking_date: date
    value_date: date
    amount: float
    currency: str
    creditor_name: str | None = None
    debtor_name: str | None = None
    remittance_information: str | None = None
    source_type: SourceType


class TransactionOut(TransactionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedTransaction(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[TransactionOut]
