from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.db.database import get_session
from app.models.models import User, Challenge, Submission
from app.schemas.submission import SubmissionCreate, SubmissionResponse, SubmissionWithChallenge
from app.utils.auth import get_current_active_user, get_current_candidate_user, get_current_company_user

router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"]
)

@router.post("/", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
def create_submission(
    submission: SubmissionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_candidate_user)
):
    # Check if challenge exists
    statement = select(Challenge).where(Challenge.id == submission.challenge_id)
    challenge = session.exec(statement).first()
    
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Challenge with ID {submission.challenge_id} not found"
        )
    
    # Create new submission
    db_submission = Submission(
        content=submission.content,
        candidate_id=current_user.id,
        challenge_id=submission.challenge_id
    )
    
    # Add submission to database
    session.add(db_submission)
    session.commit()
    session.refresh(db_submission)
    
    return db_submission

@router.get("/", response_model=List[SubmissionWithChallenge])
def get_all_submissions(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_company_user)
):
    # Get all submissions with challenge title
    statement = select(Submission, Challenge.title).join(
        Challenge, Submission.challenge_id == Challenge.id
    )
    results = session.exec(statement).all()
    
    # Format results
    submissions = []
    for submission, challenge_title in results:
        submission_dict = submission.dict()
        submission_dict["challenge_title"] = challenge_title
        submissions.append(submission_dict)
    
    return submissions

@router.get("/my", response_model=List[SubmissionWithChallenge])
def get_my_submissions(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_candidate_user)
):
    # Get all submissions for current user with challenge title
    statement = select(Submission, Challenge.title).join(
        Challenge, Submission.challenge_id == Challenge.id
    ).where(Submission.candidate_id == current_user.id)
    results = session.exec(statement).all()
    
    # Format results
    submissions = []
    for submission, challenge_title in results:
        submission_dict = submission.dict()
        submission_dict["challenge_title"] = challenge_title
        submissions.append(submission_dict)
    
    return submissions 