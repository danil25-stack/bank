from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.psu.models import Psu
from src.psu.schemas import PsuCreate
from fastapi import HTTPException


async def create_psu(db: AsyncSession, psu: PsuCreate):
    db_psu = Psu(name=psu.name, email=psu.email)
    db_psu.encrypt_fields()

    db.add(db_psu)
    await db.commit()
    await db.refresh(db_psu)

    db_psu.decrypt_fields()
    return db_psu


async def get_psu(db: AsyncSession, psu_id: int):
    result = await db.execute(select(Psu).where(Psu.id == psu_id))
    psu = result.scalar_one_or_none()
    if psu:
        psu.decrypt_fields()
    return psu


async def get_all_psu(db: AsyncSession):
    result = await db.execute(select(Psu))
    psus = result.scalars().all()
    for psu in psus:
        psu.decrypt_fields()
    return psus


async def delete_psu(db: AsyncSession, psu_id: int):
    psu = await get_psu(db, psu_id)
    if not psu:
        return False

    await db.delete(psu)
    await db.commit()
    return True
