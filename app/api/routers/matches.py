from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Dict, Any
import httpx
import os
from dotenv import load_dotenv
import json
from statistics import mean
import re
from functools import lru_cache

from app.db.database import get_session
from app.models.models import User, Challenge, Submission
from app.utils.auth import get_current_active_user, get_current_company_user

# Load environment variables
load_dotenv()

# Groq API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"  # Using Llama 3 8B model which is free and fast

router = APIRouter(
    prefix="/match",
    tags=["AI Match Suggestions"]
)

# LRU cache to avoid repeated API calls for the same content
@lru_cache(maxsize=100)
async def get_embedding_representation(text: str) -> Dict:
    """
    Get a semantic representation of text using Groq's LLM.
    This function extracts key concepts and skills from the text.
    """
    if not GROQ_API_KEY:
        # Fallback if no API key is provided
        words = re.findall(r'\w+', text.lower())
        return {word: 1 for word in set(words) if len(word) > 3}
    
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
        Extract key skills, technologies, and concepts from this text. 
        Return a JSON object where keys are the extracted terms and values are 
        confidence scores between 0 and 1.
        
        Text: {text}
        
        Format your response as valid JSON only, like this:
        {{
            "python": 0.9,
            "data analysis": 0.7
        }}
        """
        
        payload = {
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 500
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                try:
                    # Extract JSON from the response
                    json_match = re.search(r'({.*})', content.replace('\n', ''))
                    if json_match:
                        return json.loads(json_match.group(1))
                    return json.loads(content)
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails
                    words = re.findall(r'\w+', content.lower())
                    return {word: 1 for word in set(words) if len(word) > 3}
            
        # Fallback
        return {"error": 1.0}
        
    except Exception as e:
        print(f"Error in LLM processing: {str(e)}")
        # Fallback to simple keyword extraction if API call fails
        words = re.findall(r'\w+', text.lower())
        return {word: 1 for word in set(words) if len(word) > 3}

async def calculate_similarity(challenge_rep: Dict, submission_rep: Dict) -> float:
    """
    Calculate similarity between challenge and submission representations
    using a combination of keyword matching and weighted scoring.
    """
    if not challenge_rep or not submission_rep:
        return 0.0
    
    # Find common terms and calculate weighted scores
    common_terms = set(challenge_rep.keys()) & set(submission_rep.keys())
    if not common_terms:
        return 0.0
    
    # Calculate similarities for common terms
    similarities = []
    for term in common_terms:
        # Weighted by the product of both confidence scores
        weight = challenge_rep[term] * submission_rep[term]
        similarities.append(weight)
    
    # Calculate match score (average of weighted similarities)
    match_score = mean(similarities) if similarities else 0.0
    
    # Scale score based on coverage (how many terms match relative to challenge terms)
    coverage = len(common_terms) / len(challenge_rep) if challenge_rep else 0
    final_score = match_score * (0.7 + 0.3 * coverage)
    
    return min(final_score, 1.0)  # Cap at 1.0

@router.get("/suggestions", response_model=List[Dict[str, Any]])
async def get_match_suggestions(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_company_user)
):
    """
    AI-based match suggestions between challenges and submissions.
    Uses semantic analysis via LLM to find the best matches.
    """
    # Get all challenges for the current company
    statement = select(Challenge).where(Challenge.company_id == current_user.id)
    challenges = session.exec(statement).all()
    
    # Get all submissions
    statement = select(Submission).join(
        Challenge, Submission.challenge_id == Challenge.id
    ).where(Challenge.company_id != current_user.id)
    submissions = session.exec(statement).all()
    
    if not challenges or not submissions:
        return []
    
    # Process and analyze all challenges and submissions
    suggestions = []
    
    # Process each challenge-submission pair
    for challenge in challenges:
        # Get challenge representation (skills, concepts, technology requirements)
        challenge_text = f"{challenge.title} {challenge.description}"
        challenge_rep = await get_embedding_representation(challenge_text)
        
        for submission in submissions:
            # Get submission representation (skills demonstrated, approaches used)
            submission_rep = await get_embedding_representation(submission.content)
            
            # Calculate similarity score
            match_score = await calculate_similarity(challenge_rep, submission_rep)
            
            # Only include if the match is reasonably good
            if match_score > 0.3:
                # Find matched terms for explanation
                common_terms = set(challenge_rep.keys()) & set(submission_rep.keys())
                top_matches = sorted(
                    [(term, challenge_rep[term] * submission_rep[term]) for term in common_terms],
                    key=lambda x: x[1], 
                    reverse=True
                )[:3]  # Top 3 matching skills/concepts
                
                match_reason = ", ".join([term for term, _ in top_matches]) if top_matches else "Contextual similarity"
                
                suggestions.append({
                    "challenge_id": challenge.id,
                    "challenge_title": challenge.title,
                    "submission_id": submission.id,
                    "match_score": round(match_score, 2),
                    "match_reason": f"Skills/concepts match: {match_reason}"
                })
    
    # Sort by match score and return top 10
    suggestions.sort(key=lambda x: x["match_score"], reverse=True)
    return suggestions[:10] 