from pydantic import BaseModel
from datetime import date


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

    class Config:
        orm_mode = True
