from pydantic import BaseModel, EmailStr
from datetime import datetime

# Schema for creating a user (input)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Schema for reading/returning user data (output, excludes password)
class User(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    subscription_tier: str
    created_at: datetime
    # updated_at: datetime | None = None # Optional

    class Config:
        orm_mode = True # Compatibility with SQLAlchemy models 