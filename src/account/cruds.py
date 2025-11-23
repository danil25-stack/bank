from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.account.models import Account
from src.account.schemas import AccountCreate
from fastapi import HTTPException


async def create_account(db: AsyncSession, account: AccountCreate):
    db_account = Account(**account.model_dump())
    db_account.encrypt_fields()

    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    db_account.decrypt_fields()
    return db_account


async def get_account_by_id(db: AsyncSession, account_id: int):
    result = await db.execute(select(Account).where(Account.id == account_id))
    return result.scalar_one_or_none()


async def get_all_accounts(db: AsyncSession):
    result = await db.execute(select(Account))
    return result.scalars().all()


async def delete_account(db: AsyncSession, account_id: int):
    account = await get_account_by_id(db, account_id)
    if not account:
        raise HTTPException(404, "Account not found")

    await db.delete(account)
    await db.commit()
    return {"message": "Account deleted successfully"}


async def update_account(db: AsyncSession, account_id: int, data: AccountCreate):
    account = await get_account_by_id(db, account_id)
    if not account:
        raise HTTPException(404, "Account not found")

    for key, value in data.model_dump().items():
        setattr(account, key, value)

    await db.commit()
    await db.refresh(account)
    return account
