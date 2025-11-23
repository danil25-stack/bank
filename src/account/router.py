from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.account import cruds
from src.account.schemas import AccountCreate, AccountOut

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


@router.post("/", response_model=AccountOut)
async def create_account(account: AccountCreate, db: AsyncSession = Depends(get_db)):
    return await cruds.create_account(db, account)  # ⚠️ await


@router.get("/{account_id}", response_model=AccountOut)
async def get_account(account_id: int, db: AsyncSession = Depends(get_db)):
    account = await cruds.get_account_by_id(db, account_id)
    if not account:
        raise HTTPException(404, "Account not found")
    return account


@router.get("/", response_model=list[AccountOut])
async def get_all_accounts(db: AsyncSession = Depends(get_db)):
    return await cruds.get_all_accounts(db)


@router.delete("/{account_id}")
async def delete_account(account_id: int, db: AsyncSession = Depends(get_db)):
    return await cruds.delete_account(db, account_id)


@router.put("/{account_id}", response_model=AccountOut)
async def update_account(account_id: int, updated: AccountCreate, db: AsyncSession = Depends(get_db)):
    return await cruds.update_account(db, account_id, updated)
