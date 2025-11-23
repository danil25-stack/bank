from pydantic import BaseModel
from datetime import date


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

    class Config:
        orm_mode = True
