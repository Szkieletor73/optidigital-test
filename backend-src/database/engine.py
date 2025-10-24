from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# We're using a local SQLite DB, for simplicity
engine = create_engine(url="sqlite:///./database.db", echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Proper fetcher for the database session engine, so it closes gracefully
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()