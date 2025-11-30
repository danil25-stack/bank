from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.database import get_db
from src.consent.schemas import ConsentCreate, ConsentOut, ConsentUpdate, PaginatedConsent
from src.consent import cruds
from src.consent.models import Consent


router = APIRouter(prefix="/consent", tags=["Consent"])


@router.post("/", response_model=ConsentOut)
async def create(consent: ConsentCreate, db: AsyncSession = Depends(get_db)):
    return await cruds.create_consent(db, consent)


@router.get("/{consent_id}", response_model=ConsentOut)
async def read(consent_id: int, db: AsyncSession = Depends(get_db)):
    db_consent = await cruds.get_consent(db, consent_id)
    if not db_consent:
        raise HTTPException(404, "Consent not found")
    return db_consent


@router.get("/", response_model=PaginatedConsent)
async def read_all(
    skip: int = 0,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    total_query = await db.execute(select(func.count(Consent.id)))
    total = total_query.scalar()

    result = await db.execute(
        select(Consent)
        .offset(offset)
        .limit(limit)
    )
    items = result.scalars().all()

    for item in items:
        item.decrypt_fields()

    return PaginatedConsent(
        total=total,
        limit=limit,
        offset=offset,
        items=items,
    )


@router.put("/{consent_id}", response_model=ConsentOut)
async def update(consent_id: int, consent: ConsentUpdate, db: AsyncSession = Depends(get_db)):
    updated = await cruds.update_consent(db, consent_id, consent)
    if not updated:
        raise HTTPException(404, "Consent not found")
    return updated


@router.delete("/{consent_id}")
async def delete(consent_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await cruds.delete_consent(db, consent_id)
    if not deleted:
        raise HTTPException(404, "Consent not found")
    return {"message": "Consent deleted successfully"}
