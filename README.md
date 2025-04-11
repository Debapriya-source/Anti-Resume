# Skills-Based Hiring Platform API

A FastAPI-based backend API for a skills-based hiring platform that supports candidates and companies.

## Features

- JWT-based authentication with role differentiation (candidate/company)
- User registration and login
- Challenge management (create, view, list)
- Submission handling (submit solutions, view submissions)
- AI-powered match suggestions using LLM semantic analysis
- Optional file upload support for challenges and submissions

## Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Groq API key (for AI matching feature)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd massai-hackathon
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in development mode:

```bash
pip install -e .
```

4. Create a `.env` file in the root directory with the following content:

```
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./skills_platform.db
GROQ_API_KEY=your_groq_api_key_here  # Get this from https://console.groq.com/
```

## Running the Application

Run the development server:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user (candidate or company)
- `POST /auth/login` - Login and get access token

### Challenges

- `GET /challenges` - List all challenges
- `GET /challenges/{id}` - Get challenge details
- `POST /challenges` - Create a new challenge (company only)

### Submissions

- `POST /submissions` - Submit a solution (candidate only)
- `GET /submissions` - List all submissions (company only)
- `GET /submissions/my` - List user's submissions (candidate only)

### AI Match Suggestions

- `GET /match/suggestions` - Get AI-based match suggestions between challenges and submissions (company only)

This endpoint uses semantic analysis powered by Groq's LLM API to identify the best matches between company challenges and candidate submissions. It analyzes the skills, technologies, and concepts mentioned in both challenges and submissions, then calculates similarity scores to suggest the most promising candidates for each challenge.

### File Uploads

- `POST /upload/challenge/{id}/attachment` - Upload challenge attachment (company only)
- `POST /upload/submission/{id}/file` - Upload submission file (candidate only)

## Project Structure

```
.
├── app/
│   ├── api/
│   │   └── routers/
│   │       ├── auth.py
│   │       ├── challenges.py
│   │       ├── submissions.py
│   │       ├── matches.py
│   │       └── uploads.py
│   ├── core/
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   └── models.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── challenge.py
│   │   └── submission.py
│   ├── utils/
│   │   └── auth.py
│   └── main.py
├── .env
├── .gitignore
├── main.py
├── pyproject.toml
├── setup.py
└── README.md
```

## Development

The project uses:

- FastAPI for the web framework
- SQLModel for database ORM
- JWT for authentication
- Pydantic for data validation
- uvicorn for ASGI server
- Groq API for AI-powered matching
- PEP 621 compliant dependency management via pyproject.toml

## AI Matching Implementation

The AI matching system works by:

1. Analyzing challenge descriptions using LLM to extract key skills, technologies, and concepts
2. Analyzing submission content to extract demonstrated skills and approaches
3. Calculating similarity scores between challenges and submissions based on semantic overlap
4. Providing detailed match reasons based on the specific skills that aligned

This approach enables companies to find the most qualified candidates based on the content of their submissions rather than simple keyword matching.

## Security Notes

- In production, replace the secret key with a secure value
- Configure CORS settings appropriately
- Use HTTPS in production
- Consider rate limiting and other security measures
- Store sensitive data securely
- Implement proper error handling and logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
