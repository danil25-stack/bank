from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.psu.models import Psu
from src.loan.models import Loan
from src.loan.schemas import LoanCreate


class CreateLoanService:

    def __init__(self, db: AsyncSession, loan_data: LoanCreate):
        self._db = db
        self._loan_data = loan_data

    async def create(self) -> Loan:
        await self._validate()
        return await self._create_model_instance()

    async def _create_model_instance(self) -> Loan:
        db_loan = Loan(
            psu_id=self._loan_data.psu_id,
            repayment_account_id=self._loan_data.repayment_account_id,
            principal_amount=self._loan_data.principal_amount,
            currency=self._loan_data.currency,
            interest_rate=self._loan_data.interest_rate,
            term_months=self._loan_data.term_months,
            start_date=self._loan_data.start_date,
            end_date=self._loan_data.end_date,
            status=self._loan_data.status,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db_loan.encrypt_fields()
        self._db.add(db_loan)

        await self._db.commit()
        await self._db.refresh(db_loan)

        db_loan.decrypt_fields()
        return db_loan

    async def _validate(self) -> None:
        result = await self._db.execute(
            select(Psu).where(Psu.id == self._loan_data.psu_id)
        )
        psu = result.scalar_one_or_none()

        if not psu:
            raise HTTPException(
                status_code=404,
                detail=f"PSU with id {self._loan_data.psu_id} does not exist"
            )


async def get_loan(db: AsyncSession, loan_id: int):
    result = await db.execute(select(Loan).where(Loan.id == loan_id))
    return result.scalar_one_or_none()


async def get_all_loans(db: AsyncSession):
    result = await db.execute(select(Loan))
    return result.scalars().all()


async def update_loan(db: AsyncSession, loan_id: int, updated_data: dict):
    loan = await get_loan(db, loan_id)
    if not loan:
        return None

    for key, value in updated_data.items():
        setattr(loan, key, value)

    loan.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(loan)
    return loan


async def delete_loan(db: AsyncSession, loan_id: int):
    loan = await get_loan(db, loan_id)
    if not loan:
        return False

    await db.delete(loan)
    await db.commit()
    return True
