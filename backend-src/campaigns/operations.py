from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from campaigns.models import Campaign as CampaignModel
from campaigns.schemas import Campaign as CampaignSchema
from database.engine import get_db
from auth.schemas import User as UserSchema
from auth.auth import get_current_user

not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="The resource you were trying to request was not found."
)

# Unlike in auth.auth, here we use a DB session passed by the FastAPI dependency from the endpoint handler.
# This is because, at least at this level of complexity, we're not going to deal with many nested function calls that need DB session handles.

# Get a list of all campaigns.
def get_campaigns(db: Session):
    return db.query(CampaignModel).all()

# Get details of a specific campaign
def get_campaign(id: int, db: Session):
    campaign = db.query(CampaignModel).filter(CampaignModel.id == id).first()
    if not campaign:
        raise not_found_exception
    return campaign

# Create a new campaign
# Returns the inserted campaign, or the proper error (internal server error or malformed request)
def create_campaign(campaign_data: CampaignSchema, db: Session):
    campaign = CampaignModel(**campaign_data.model_dump(exclude={"id"}))
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign

# Update an existing campaign
def update_campaign(id: int, new_data: CampaignSchema, db: Session):
    campaign = db.query(CampaignModel).filter(CampaignModel.id == id).first()
    if not campaign:
        raise not_found_exception
    
    # Replace values in the existing entry with new ones
    for key, value in new_data.model_dump(exclude={"id"}).items():
        setattr(campaign, key, value)

    # The commit will update the existing entry, as we're working with a handle to the specific DB row.
    db.commit()
    db.refresh(campaign)
    return campaign

# Delete a campaign
def delete_campaign(id: int, db: Session):
    campaign = db.query(CampaignModel).filter(CampaignModel.id == id).first()
    if not campaign:
        raise not_found_exception
    
    db.delete(campaign)
    db.commit()
    return {"message": "Campaign deleted successfully"}