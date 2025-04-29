from fastapi import APIRouter, Depends

from .. import models, security
from ..models.user import User as UserModel
from ..schemas import user as user_schemas # Import user schema module

router = APIRouter(
    prefix="/users", # Add prefix for all routes in this router
    tags=["Users"]
)

@router.get("/me", response_model=user_schemas.User)
async def read_users_me(current_user: UserModel = Depends(security.get_current_active_user)):
    """Fetches the details for the currently logged-in user."""
    # Type hint for current_user is now UserModel as returned by dependency
    # but FastAPI uses the response_model for output serialization
    return current_user

# Add other user-related endpoints here later (e.g., update profile) 