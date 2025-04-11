from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from dotenv import load_dotenv
import os

from app.db.database import get_session
from app.models.models import User
from app.schemas.user import TokenData

# Load environment variables
load_dotenv()

# Get environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash password
def get_password_hash(password):
    return pwd_context.hash(password)

# Function to authenticate user
def authenticate_user(session: Session, email: str, password: str):
    # Get user by email
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    
    # If user not found or password incorrect, return None
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    return user

# Function to create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Encode token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

# Function to get current user
async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        
        if email is None:
            raise credentials_exception
        
        token_data = TokenData(email=email, role=role)
    except JWTError:
        raise credentials_exception
    
    # Get user by email
    statement = select(User).where(User.email == token_data.email)
    user = session.exec(statement).first()
    
    if user is None:
        raise credentials_exception
    
    return user

# Function to get current active user
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user

# Function to check if user is company
async def get_current_company_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "company":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Only company users can access this endpoint."
        )
    return current_user

# Function to check if user is candidate
async def get_current_candidate_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "candidate":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Only candidate users can access this endpoint."
        )
    return current_user 