from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./skills_platform.db")

# Create SQLModel engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Function to create database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Function to get database session
def get_session():
    with Session(engine) as session:
        yield session 