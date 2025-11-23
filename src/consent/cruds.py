# crud/consent.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from fastapi import HTTPException

from src.consent.models import Consent
from src.consent.schemas import ConsentCreate, ConsentUpdate


async def create_consent(db: AsyncSession, consent: ConsentCreate):
    db_consent = Consent(**consent.model_dump())
    db_consent.encrypt_fields()

    db.add(db_consent)
    await db.commit()
    await db.refresh(db_consent)
    db_consent.decrypt_fields()
    return db_consent


async def get_consent(db: AsyncSession, consent_id: int):
    result = await db.execute(select(Consent).where(Consent.id == consent_id))
    return result.scalar_one_or_none()


async def get_consents(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Consent).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def update_consent(db: AsyncSession, consent_id: int, consent: ConsentUpdate):
    db_consent = await get_consent(db, consent_id)
    if not db_consent:
        return None

    for field, value in consent.model_dump(exclude_unset=True).items():
        setattr(db_consent, field, value)

    db_consent.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(db_consent)
    return db_consent


async def delete_consent(db: AsyncSession, consent_id: int):
    db_consent = await get_consent(db, consent_id)
    if not db_consent:
        return False

    await db.delete(db_consent)
    await db.commit()
    return True
