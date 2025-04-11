from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# User model
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = Field(default="candidate")  # "candidate" or "company"
    
    # Relationships
    challenges: List["Challenge"] = Relationship(back_populates="company")
    submissions: List["Submission"] = Relationship(back_populates="candidate")

# Challenge model
class Challenge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    company_id: int = Field(foreign_key="user.id")
    
    # Relationships
    company: User = Relationship(back_populates="challenges")
    submissions: List["Submission"] = Relationship(back_populates="challenge")

# Submission model
class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    candidate_id: int = Field(foreign_key="user.id")
    challenge_id: int = Field(foreign_key="challenge.id")
    
    # Relationships
    candidate: User = Relationship(back_populates="submissions")
    challenge: Challenge = Relationship(back_populates="submissions") 