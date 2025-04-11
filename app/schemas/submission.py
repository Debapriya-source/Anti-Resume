from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base submission schema
class SubmissionBase(BaseModel):
    content: str

# Submission creation schema
class SubmissionCreate(SubmissionBase):
    challenge_id: int

# Submission response schema
class SubmissionResponse(SubmissionBase):
    id: int
    timestamp: datetime
    candidate_id: int
    challenge_id: int
    
    class Config:
        from_attributes = True

# Submission with challenge info
class SubmissionWithChallenge(SubmissionResponse):
    challenge_title: str
    
    class Config:
        from_attributes = True 