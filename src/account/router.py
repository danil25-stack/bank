from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.database import get_db
from src.account import cruds
from src.account.schemas import AccountCreate, AccountOut, PaginatedAccount
from src.auth.schemas import User
from src.auth.middleware import get_current_user
from src.account.models import Account

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


@router.post("/", response_model=AccountOut)
async def create_account(
    account: AccountCreate,
    db: AsyncSession = Depends(get_db),
    # user: User = Depends(get_current_user)
):
    return await cruds.create_account(db, account)


@router.get("/{account_id}", response_model=AccountOut)
async def get_account(
    account_id: int,
    db: AsyncSession = Depends(get_db),
    # user: User = Depends(get_current_user)
):
    account = await cruds.get_account_by_id(db, account_id)
    if not account:
        raise HTTPException(404, "Account not found")
    return account


@router.get("/", response_model=PaginatedAccount)
async def get_all_accounts(
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    # user: User = Depends(get_current_user)
):
    total_query = await db.execute(select(func.count(Account.id)))
    total = total_query.scalar()

    result = await db.execute(
        select(Account)
        .offset(offset)
        .limit(limit)
    )
    items = result.scalars().all()

    for item in items:
        item.decrypt_fields()

    return PaginatedAccount(
        total=total,
        limit=limit,
        offset=offset,
        items=items
    )


@router.delete("/{account_id}")
async def delete_account(
    account_id: int,
    db: AsyncSession = Depends(get_db),
    # user: User = Depends(get_current_user)
):
    return await cruds.delete_account(db, account_id)


@router.put("/{account_id}", response_model=AccountOut)
async def update_account(
    account_id: int,
    updated: AccountCreate,
    db: AsyncSession = Depends(get_db),
    # user: User = Depends(get_current_user)
):
    return await cruds.update_account(db, account_id, updated)
