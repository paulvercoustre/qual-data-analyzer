from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# from .. import database, models, schemas, security # Use relative imports
# from .. import database, models, security # Adjusted import
from .. import database, security # Further adjusted import
from ..models import user as user_model # Import the user model specifically
from ..schemas import user as user_schemas
from ..schemas import token as token_schemas

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/register", response_model=user_schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: user_schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Check if user already exists
    db_user = db.query(user_model.User).filter(user_model.User.email == user.email).first() # Use imported model
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = security.get_password_hash(user.password)
    
    # Create new user instance
    db_user = user_model.User(email=user.email, hashed_password=hashed_password) # Use imported model
    
    # Add user to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=token_schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(user_model.User).filter(user_model.User.email == form_data.username).first() # Use imported model
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )

    # Create access token (store user ID in 'sub' claim)
    access_token = security.create_access_token(
        data={"sub": str(user.id)} 
    )
    return {"access_token": access_token, "token_type": "bearer"} 