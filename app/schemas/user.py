from pydantic import BaseModel, EmailStr
from typing import Optional

# Base user schema
class UserBase(BaseModel):
    email: EmailStr
    role: str = "candidate"  # Default role is candidate

# User creation schema
class UserCreate(UserBase):
    password: str

# User response schema (without password)
class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

# User login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Token data schema
class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None 