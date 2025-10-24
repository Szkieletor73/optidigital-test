from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# We're using a local SQLite DB, for simplicity
engine = create_engine(url="sqlite:///./database.db", echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Proper generator for the database session engine to share connections when needed.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()