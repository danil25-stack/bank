from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import List


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

    model_config = ConfigDict(from_attributes=True)


class PaginatedLoan(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[LoanOut]
