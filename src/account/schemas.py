from pydantic import BaseModel


class AccountCreate(BaseModel):
    resource_id: int
    iban: str
    currency: str
    product: str
    cash_account_type: str
    name: str
    psu_id: int


class AccountOut(AccountCreate):
    id: int

    class Config:
        orm_mode = True
