from pydantic import BaseModel
from typing import Optional, List

# Base challenge schema
class ChallengeBase(BaseModel):
    title: str
    description: str

# Challenge creation schema
class ChallengeCreate(ChallengeBase):
    pass

# Challenge response schema
class ChallengeResponse(ChallengeBase):
    id: int
    company_id: int
    
    class Config:
        from_attributes = True

# Challenge with company info
class ChallengeWithCompany(ChallengeResponse):
    company_email: str
    
    class Config:
        from_attributes = True 