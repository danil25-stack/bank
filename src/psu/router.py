from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.database import get_db
from src.psu import cruds
from src.psu.schemas import PsuCreate, PsuOut, PaginatedPsu
from src.psu.models import Psu


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


@router.get("/", response_model=PaginatedPsu)
async def get_all_psu(
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    total_query = await db.execute(select(func.count(Psu.id)))
    total = total_query.scalar()

    result = await db.execute(
        select(Psu)
        .offset(offset)
        .limit(limit)
    )

    items = result.scalars().all()

    for item in items:
        item.decrypt_fields()
    psu_out_list = [PsuOut.model_validate(psu) for psu in items]
    return PaginatedPsu(
        total=total,
        limit=limit,
        offset=offset,
        items=psu_out_list,
    )


@router.delete("/{psu_id}")
async def delete_psu(psu_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await cruds.delete_psu(db, psu_id)
    if not deleted:
        raise HTTPException(404, "PSU not found")
    return {"message": "PSU deleted successfully"}
