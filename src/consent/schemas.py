from datetime import date, datetime
from typing import Optional, Dict
from pydantic import BaseModel


class ConsentBase(BaseModel):
    psu_id: int
    access: Optional[Dict] = None
    recurring_indicator: Optional[bool] = False
    valid_until: Optional[date] = None
    frequency_per_day: Optional[int] = None
    combined_service_indicator: Optional[bool] = False
    status: str


class ConsentCreate(ConsentBase):
    pass


class ConsentUpdate(BaseModel):
    access: Optional[Dict] = None
    recurring_indicator: Optional[bool] = None
    valid_until: Optional[date] = None
    frequency_per_day: Optional[int] = None
    combined_service_indicator: Optional[bool] = None
    status: Optional[str] = None


class ConsentOut(ConsentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
