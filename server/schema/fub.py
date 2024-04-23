from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class FubBaseInfoSchema(BaseModel):
    id: int
    name: str
    code: str
    lat: float
    lon: float
    sort: int
    is_del: bool
    fub_type: int
    fub_kind: int

    class Config:
        orm_mode = True
