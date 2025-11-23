from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.loan_schedule.models import LoanRepaymentScheduleItem
from src.loan_schedule.schemas import LoanScheduleCreate


async def create_schedule_item(db: AsyncSession, item: LoanScheduleCreate):
    db_item = LoanRepaymentScheduleItem(**item.model_dump())
    db_item.encrypt_fields()

    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)

    db_item.decrypt_fields()
    return db_item


async def get_schedule_item(db: AsyncSession, item_id: int):
    result = await db.execute(
        select(LoanRepaymentScheduleItem).where(
            LoanRepaymentScheduleItem.id == item_id)
    )
    return result.scalar_one_or_none()


async def get_all_schedule_items(db: AsyncSession):
    result = await db.execute(select(LoanRepaymentScheduleItem))
    return result.scalars().all()


async def delete_schedule_item(db: AsyncSession, item_id: int):
    item = await get_schedule_item(db, item_id)
    if not item:
        return False

    await db.delete(item)
    await db.commit()
    return True
