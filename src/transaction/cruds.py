from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.transaction.models import Transaction
from src.transaction.schemas import TransactionCreate


async def create_transaction(db: AsyncSession, transaction: TransactionCreate):
    db_tx = Transaction(**transaction.model_dump())   # Pydantic v2
    db_tx.encrypt_fields()

    db.add(db_tx)
    await db.commit()
    await db.refresh(db_tx)

    db_tx.decrypt_fields()
    return db_tx


async def get_transaction(db: AsyncSession, tx_id: int):
    result = await db.execute(select(Transaction).where(Transaction.id == tx_id))
    return result.scalar_one_or_none()


async def get_all_transactions(db: AsyncSession):
    result = await db.execute(select(Transaction))
    return result.scalars().all()


async def delete_transaction(db: AsyncSession, tx_id: int):
    tx = await get_transaction(db, tx_id)
    if not tx:
        return False

    await db.delete(tx)
    await db.commit()
    return True
