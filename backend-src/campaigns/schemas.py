from datetime import datetime
from pydantic import BaseModel


class CampaignBase(BaseModel):
    id: int

class Campaign(CampaignBase):
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    budget: float
    status: bool

    class Config:
        from_attributes = True