from pydantic import BaseModel
from datetime import date, datetime


class LoanBase(BaseModel):
    psu_id: int
    repayment_account_id: int
    principal_amount: float
    currency: str
    interest_rate: float
    term_months: int
    start_date: date
    end_date: date
    status: str


class LoanCreate(LoanBase):
    pass


class LoanOut(LoanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
