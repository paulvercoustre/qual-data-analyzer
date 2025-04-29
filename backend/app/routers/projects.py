from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Use relative imports for models, schemas, security, and dependencies
from .. import models, security
from ..schemas import project as project_schemas # Alias to avoid naming conflict
from ..database import get_db

# Import the specific User model for type hinting
from ..models.user import User as UserModel

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    dependencies=[Depends(security.get_current_active_user)], # Apply auth to all routes in this router
    responses={404: {"description": "Not found"}}, # Default response for not found
)

@router.post("/", response_model=project_schemas.Project, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: project_schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(security.get_current_active_user) # Get current user
):
    """
    Creates a new project for the currently authenticated user.
    """
    # Create a new Project database model instance
    db_project = models.project.Project(
        **project.model_dump(), # Unpack validated data from Pydantic model
        owner_id=current_user.id # Set the owner to the current user
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project) # Refresh to get the generated ID and defaults
    return db_project

@router.get("/", response_model=List[project_schemas.Project])
async def read_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(security.get_current_active_user)
):
    """
    Retrieves a list of projects owned by the currently authenticated user.
    """
    projects = (
        db.query(models.project.Project)
        .filter(models.project.Project.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return projects

# Add other project-related endpoints here later (e.g., get by ID, update, delete)
# @router.get("/{project_id}", response_model=project_schemas.Project) ...
# @router.put("/{project_id}", response_model=project_schemas.Project) ...
# @router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT) ... 