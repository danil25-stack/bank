from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.database import get_db
from src.consent.schemas import ConsentCreate, ConsentOut, ConsentUpdate
from src.consent import cruds

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


@router.get("/", response_model=List[ConsentOut])
async def read_all(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await cruds.get_consents(db, skip, limit)


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
