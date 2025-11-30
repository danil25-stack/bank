from pydantic import BaseModel, ConfigDict
from typing import List


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

    model_config = ConfigDict(from_attributes=True)


class PaginatedAccount(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[AccountOut]
