from sqlalchemy.orm import Session
from campaigns.models import Base as CampaignsBase
from auth.models import Base as AuthBase, User
from auth.auth import get_hash
from database.engine import engine

def initialize_db():
    # Initializes the database
    AuthBase.metadata.create_all(bind=engine)
    CampaignsBase.metadata.create_all(bind=engine)

    # Create a demo user
    with Session(engine) as session:
        try:
            hashed = get_hash("admin")
            demo_user = User(
                username="admin",
                password_hash=hashed
            )
            session.add(demo_user)
            session.commit()
        except:
            pass