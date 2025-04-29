from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating a project (input)
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None # Optional field

# Schema for reading/returning project data (output)
class Project(ProjectCreate):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        # Enable ORM mode to work with SQLAlchemy models
        # For Pydantic V2, use from_attributes=True
        from_attributes = True
        # orm_mode = True # For Pydantic V1 