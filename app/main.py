from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import create_db_and_tables
from app.api.routers import auth, challenges, submissions, matches, uploads

# Create FastAPI app
app = FastAPI(
    title="Skills-Based Hiring Platform API",
    description="API for a skills-based hiring platform that supports candidates and companies",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(challenges.router)
app.include_router(submissions.router)
app.include_router(matches.router)  # Optional AI match suggestions
app.include_router(uploads.router)  # Optional file uploads

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Skills-Based Hiring Platform API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 