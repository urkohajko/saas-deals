from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Deal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    price: float
    url: str
    category: str
    image_url: str
    discount_percent: int
    coupon_code: Optional[str] = None
    popularity: int = 0
    clicks: int = 0
    created_at: datetime
