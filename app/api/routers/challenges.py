from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.db.database import get_session
from app.models.models import User, Challenge
from app.schemas.challenge import ChallengeCreate, ChallengeResponse, ChallengeWithCompany
from app.utils.auth import get_current_active_user, get_current_company_user

router = APIRouter(
    prefix="/challenges",
    tags=["Challenges"]
)

@router.get("/", response_model=List[ChallengeWithCompany])
def get_all_challenges(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    # Get all challenges with company email
    statement = select(Challenge, User.email).join(User, Challenge.company_id == User.id)
    results = session.exec(statement).all()
    
    # Format results
    challenges = []
    for challenge, company_email in results:
        challenge_dict = challenge.dict()
        challenge_dict["company_email"] = company_email
        challenges.append(challenge_dict)
    
    return challenges

@router.get("/{challenge_id}", response_model=ChallengeWithCompany)
def get_challenge(
    challenge_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    # Get challenge with company email
    statement = select(Challenge, User.email).join(
        User, Challenge.company_id == User.id
    ).where(Challenge.id == challenge_id)
    
    result = session.exec(statement).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Challenge with ID {challenge_id} not found"
        )
    
    challenge, company_email = result
    
    # Format result
    challenge_dict = challenge.dict()
    challenge_dict["company_email"] = company_email
    
    return challenge_dict

@router.post("/", response_model=ChallengeResponse, status_code=status.HTTP_201_CREATED)
def create_challenge(
    challenge: ChallengeCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_company_user)
):
    # Create new challenge
    db_challenge = Challenge(
        title=challenge.title,
        description=challenge.description,
        company_id=current_user.id
    )
    
    # Add challenge to database
    session.add(db_challenge)
    session.commit()
    session.refresh(db_challenge)
    
    return db_challenge 