from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List


class LoanScheduleCreate(BaseModel):
    loan_id: int
    installment_number: int
    due_date: date
    principal_due: float
    interest_due: float
    total_due: float
    paid: bool = False
    paid_date: date | None = None


class LoanScheduleOut(LoanScheduleCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedLoanSchedule(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[LoanScheduleOut]
