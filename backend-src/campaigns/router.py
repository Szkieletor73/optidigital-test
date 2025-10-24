from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated, List
from campaigns.schemas import Campaign as CampaignSchema
from database.engine import get_db
from auth.schemas import User as UserSchema
from auth.auth import get_current_user
import campaigns.operations as operations

router = APIRouter(
    prefix="/campaigns",
    responses={404: {"description": "Not Found"}, 401: {"description": "Unauthorized"}}
)

# We're using the `user` dependency as a Route Guard. If it fails, that's because the user is not authenticated,
# and so they won't be able to access these routes.

# Get a list of all campaigns
@router.get("/", response_model=List[CampaignSchema])
def get_campaigns(user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    return operations.get_campaigns(db)

# Get a singular campaign
@router.get("/{campaign_id}", response_model=CampaignSchema)
def get_campaign(campaign_id: int, user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    return operations.get_campaign(campaign_id, db)

# Create a new campaign
@router.post("/", response_model=CampaignSchema)
def create_campaign(campaign: CampaignSchema, user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    return operations.create_campaign(campaign, db)

# Update an existing campaign
# We're fetching the campaign ID from the URL, because it's cleaner in terms of logging and debugging, and CampaignSchema doesn't always contain an ID.
@router.put("/{campaign_id}", response_model=CampaignSchema)
def update_campaign(campaign_id: int, campaign: CampaignSchema, user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    return operations.update_campaign(campaign_id, campaign, db)

# Delete an existing campaign
@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int, user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    return operations.delete_campaign(campaign_id, db)