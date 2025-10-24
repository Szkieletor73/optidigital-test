from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Campaign(BaseModel):
    id: Optional[int] | None
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    budget: float
    status: bool

    class Config:
        from_attributes = True