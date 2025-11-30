from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.database import get_db
from src.loan import cruds
from src.loan.schemas import LoanCreate, LoanOut, PaginatedLoan
from src.loan.models import Loan

router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


@router.post("/", response_model=LoanOut)
async def create_loan(loan: LoanCreate, db: AsyncSession = Depends(get_db)):
    service = cruds.CreateLoanService(db, loan)
    return await service.create()


@router.get("/{loan_id}", response_model=LoanOut)
async def get_loan(loan_id: int, db: AsyncSession = Depends(get_db)):
    loan = await cruds.get_loan(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan


@router.get("/", response_model=PaginatedLoan)
async def get_all_loans(
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    total_query = await db.execute(select(func.count(Loan.id)))
    total = total_query.scalar()

    result = await db.execute(
        select(Loan)
        .offset(offset)
        .limit(limit)
    )
    items = result.scalars().all()

    for item in items:
        item.decrypt_fields()

    return PaginatedLoan(
        total=total,
        limit=limit,
        offset=offset,
        items=items,
    )


@router.delete("/{loan_id}")
async def delete_loan(loan_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await cruds.delete_loan(db, loan_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Loan not found")
    return {"message": "Loan deleted successfully"}


@router.put("/{loan_id}", response_model=LoanOut)
async def update_loan(loan_id: int, loan: LoanCreate, db: AsyncSession = Depends(get_db)):
    updated = await cruds.update_loan(db, loan_id, loan.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Loan not found")
    return updated
