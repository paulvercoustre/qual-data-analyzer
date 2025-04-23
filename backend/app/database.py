from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()

# Dependency for FastAPI routes to get DB session (optional but good practice)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 