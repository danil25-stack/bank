from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.psu import cruds
from src.psu.schemas import PsuCreate, PsuOut

router = APIRouter(
    prefix="/psu",
    tags=["PSU"]
)


@router.post("/", response_model=PsuOut)
async def create_psu(psu: PsuCreate, db: AsyncSession = Depends(get_db)):
    return await cruds.create_psu(db, psu)


@router.get("/{psu_id}", response_model=PsuOut)
async def get_psu(psu_id: int, db: AsyncSession = Depends(get_db)):
    psu = await cruds.get_psu(db, psu_id)
    if not psu:
        raise HTTPException(404, "PSU not found")
    return psu


@router.get("/", response_model=list[PsuOut])
async def get_all_psu(db: AsyncSession = Depends(get_db)):
    return await cruds.get_all_psu(db)


@router.delete("/{psu_id}")
async def delete_psu(psu_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await cruds.delete_psu(db, psu_id)
    if not deleted:
        raise HTTPException(404, "PSU not found")
    return {"message": "PSU deleted successfully"}
