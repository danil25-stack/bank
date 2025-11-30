from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.database import get_db
from src.loan_schedule import cruds
from src.loan_schedule.schemas import LoanScheduleCreate, LoanScheduleOut, PaginatedLoanSchedule
from src.loan_schedule.models import LoanRepaymentScheduleItem

router = APIRouter(
    prefix="/loan-schedule",
    tags=["Loan Repayment Schedule"]
)


@router.post("/", response_model=LoanScheduleOut)
async def create_schedule_item_route(item: LoanScheduleCreate, db: AsyncSession = Depends(get_db)):
    return await cruds.create_schedule_item(db, item)


@router.get("/{item_id}", response_model=LoanScheduleOut)
async def get_schedule_item_route(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await cruds.get_schedule_item(db, item_id)
    if not item:
        raise HTTPException(404, "Schedule item not found")
    return item


@router.get("/", response_model=PaginatedLoanSchedule)
async def get_all_schedule_items_route(
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    total_query = await db.execute(select(func.count(LoanRepaymentScheduleItem.id)))
    total = total_query.scalar()

    result = await db.execute(
        select(LoanRepaymentScheduleItem)
        .offset(offset)
        .limit(limit)
    )
    items = result.scalars().all()

    for item in items:
        item.decrypt_fields()

    return PaginatedLoanSchedule(
        total=total,
        limit=limit,
        offset=offset,
        items=items,
    )


@router.delete("/{item_id}")
async def delete_schedule_item_route(item_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await cruds.delete_schedule_item(db, item_id)
    if not deleted:
        raise HTTPException(404, "Schedule item not found")
    return {"message": "Schedule item deleted successfully"}
