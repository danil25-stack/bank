from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List


class PsuCreate(BaseModel):
    name: str
    email: EmailStr
    psu_number: int


class PsuOut(PsuCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedPsu(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[PsuOut]
