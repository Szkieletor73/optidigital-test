from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated, List
from campaigns.models import Campaign as CampaignModel
from campaigns.schemas import Campaign as CampaignSchema
from database.engine import get_db
from auth.schemas import User as UserSchema
from auth.auth import get_current_user

router = APIRouter(
    prefix="/campaigns",
    responses={404: {"description": "Not Found"}}
)

# Get a list of all campaigns
@router.get("/", response_model=List[CampaignSchema])
def get_campaigns(user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    return db.query(CampaignModel).all()

# Get a singular campaign
@router.get("/{campaign_id}", response_model=CampaignSchema)
def get_campaign(campaign_id: int, user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    campaign = db.query(CampaignModel).filter(CampaignModel.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

# Create a new campaign
@router.post("/", response_model=CampaignSchema)
def create_campaign(campaign: CampaignSchema, user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    db_campaign = CampaignModel(**campaign.dict(exclude={"id"}))
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

# Update an existing campaign
@router.put("/{campaign_id}", response_model=CampaignSchema)
def update_campaign(campaign_id: int, campaign: CampaignSchema, user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    db_campaign = db.query(CampaignModel).filter(CampaignModel.id == campaign_id).first()
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    for key, value in campaign.dict(exclude={"id"}).items():
        setattr(db_campaign, key, value)
    
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

# Delete an existing campaign
@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int, user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    campaign = db.query(CampaignModel).filter(CampaignModel.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    db.delete(campaign)
    db.commit()
    return {"message": "Campaign deleted successfully"}