from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from src.balance.models import Balance
from src.balance.schemas import BalanceCreate


async def create_balance(db: AsyncSession, balance: BalanceCreate):
    db_balance = Balance(**balance.model_dump())
    db_balance.encrypt_fields()

    db.add(db_balance)
    await db.commit()
    await db.refresh(db_balance)
    db_balance.decrypt_fields()
    return db_balance


async def get_balance(db: AsyncSession, balance_id: int):
    result = await db.execute(select(Balance).where(Balance.id == balance_id))
    return result.scalar_one_or_none()


async def get_all_balances(db: AsyncSession):
    result = await db.execute(select(Balance))
    return result.scalars().all()


async def delete_balance(db: AsyncSession, balance_id: int):
    balance = await get_balance(db, balance_id)
    if not balance:
        return False

    await db.delete(balance)
    await db.commit()
    return True
