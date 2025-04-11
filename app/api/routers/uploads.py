from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlmodel import Session, select
from typing import List
import os
import shutil
from pathlib import Path

from app.db.database import get_session
from app.models.models import User, Challenge, Submission
from app.utils.auth import get_current_active_user, get_current_candidate_user, get_current_company_user

router = APIRouter(
    prefix="/upload",
    tags=["File Uploads"]
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Create subdirectories for different types of uploads
CHALLENGE_ATTACHMENTS_DIR = UPLOAD_DIR / "challenge_attachments"
CHALLENGE_ATTACHMENTS_DIR.mkdir(exist_ok=True)

SUBMISSION_FILES_DIR = UPLOAD_DIR / "submission_files"
SUBMISSION_FILES_DIR.mkdir(exist_ok=True)

@router.post("/challenge/{challenge_id}/attachment")
async def upload_challenge_attachment(
    challenge_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_company_user)
):
    """
    OPTIONAL FEATURE: Upload attachment for a challenge.
    """
    # Check if challenge exists and belongs to the current company
    statement = select(Challenge).where(
        Challenge.id == challenge_id,
        Challenge.company_id == current_user.id
    )
    challenge = session.exec(statement).first()
    
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Challenge with ID {challenge_id} not found or you don't have permission to upload attachments"
        )
    
    # Create directory for this challenge if it doesn't exist
    challenge_dir = CHALLENGE_ATTACHMENTS_DIR / str(challenge_id)
    challenge_dir.mkdir(exist_ok=True)
    
    # Save file
    file_path = challenge_dir / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "filename": file.filename,
        "path": str(file_path),
        "message": "File uploaded successfully"
    }

@router.post("/submission/{submission_id}/file")
async def upload_submission_file(
    submission_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_candidate_user)
):
    """
    OPTIONAL FEATURE: Upload file for a submission.
    """
    # Check if submission exists and belongs to the current user
    statement = select(Submission).where(
        Submission.id == submission_id,
        Submission.candidate_id == current_user.id
    )
    submission = session.exec(statement).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submission with ID {submission_id} not found or you don't have permission to upload files"
        )
    
    # Create directory for this submission if it doesn't exist
    submission_dir = SUBMISSION_FILES_DIR / str(submission_id)
    submission_dir.mkdir(exist_ok=True)
    
    # Save file
    file_path = submission_dir / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "filename": file.filename,
        "path": str(file_path),
        "message": "File uploaded successfully"
    } 