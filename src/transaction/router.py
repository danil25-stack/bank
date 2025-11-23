from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.transaction import cruds
from src.transaction.schemas import TransactionCreate, TransactionOut

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("/", response_model=TransactionOut)
async def create_transaction_route(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_db)
):
    return await cruds.create_transaction(db, transaction)


@router.get("/{tx_id}", response_model=TransactionOut)
async def get_transaction_route(tx_id: int, db: AsyncSession = Depends(get_db)):
    tx = await cruds.get_transaction(db, tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx


@router.get("/", response_model=list[TransactionOut])
async def get_all_transactions_route(db: AsyncSession = Depends(get_db)):
    return await cruds.get_all_transactions(db)


@router.delete("/{tx_id}")
async def delete_transaction_route(tx_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await cruds.delete_transaction(db, tx_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}
