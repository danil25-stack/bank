from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.balance import cruds
from src.balance.schemas import BalanceCreate, BalanceOut

router = APIRouter(
    prefix="/balances",
    tags=["Balances"]
)


@router.post("/", response_model=BalanceOut)
async def create_balance(balance: BalanceCreate, db: AsyncSession = Depends(get_db)):
    return await cruds.create_balance(db, balance)


@router.get("/{balance_id}", response_model=BalanceOut)
async def get_balance(balance_id: int, db: AsyncSession = Depends(get_db)):
    balance = await cruds.get_balance(db, balance_id)
    if not balance:
        raise HTTPException(status_code=404, detail="Balance not found")
    return balance


@router.get("/", response_model=list[BalanceOut])
async def get_all_balances(db: AsyncSession = Depends(get_db)):
    return await cruds.get_all_balances(db)


@router.delete("/{balance_id}")
async def delete_balance(balance_id: int, db: AsyncSession = Depends(get_db)):
    result = await cruds.delete_balance(db, balance_id)
    if not result:
        raise HTTPException(status_code=404, detail="Balance not found")
    return {"message": "Balance deleted successfully"}
