from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import database, schemas
from .models import user as user_model # Import user model directly
from .config import settings

# OAuth2 scheme definition (points to the login endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Password Hashing Context (using bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Password Utilities ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# --- JWT Utilities ---

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Token Dependency ---

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)) -> user_model.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        # We can use TokenData schema here for validation if needed later
        # token_data = schemas.TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    user = db.query(user_model.User).filter(user_model.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: user_model.User = Depends(get_current_user)) -> user_model.User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

# Removed decode_access_token and get_user_id_from_token as their logic is now within get_current_user
# def decode_access_token(token: str) -> Optional[dict]:
#     # ... (old code)

# def get_user_id_from_token(token: str) -> Optional[int]:
#     # ... (old code) 