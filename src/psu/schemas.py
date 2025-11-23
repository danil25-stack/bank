from pydantic import BaseModel, EmailStr


class PsuCreate(BaseModel):
    name: str
    email: EmailStr


class PsuOut(PsuCreate):
    id: int

    class Config:
        orm_mode = True
