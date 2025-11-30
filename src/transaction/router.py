from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.database import get_db
from src.transaction import cruds
from src.transaction.schemas import TransactionCreate, TransactionOut, PaginatedTransaction
from src.transaction.models import Transaction


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


@router.get("/", response_model=PaginatedTransaction)
async def get_all_transactions_route(
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    total_query = await db.execute(select(func.count(Transaction.id)))
    total = total_query.scalar()

    result = await db.execute(
        select(Transaction)
        .offset(offset)
        .limit(limit)
    )
    items = result.scalars().all()
    for item in items:
        item.decrypt_fields()

    return PaginatedTransaction(
        total=total,
        limit=limit,
        offset=offset,
        items=items,
    )


@router.delete("/{tx_id}")
async def delete_transaction_route(tx_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await cruds.delete_transaction(db, tx_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}
