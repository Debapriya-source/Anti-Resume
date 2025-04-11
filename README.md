# Skills-Based Hiring Platform API

A FastAPI-based backend API for a skills-based hiring platform that supports candidates and companies.

## Features

- JWT-based authentication with role differentiation (candidate/company)
- User registration and login
- Challenge management (create, view, list)
- Submission handling (submit solutions, view submissions)
- Optional AI match suggestions
- Optional file upload support for challenges and submissions

## Prerequisites

- Python 3.12 or higher
- pip (Python package manager)

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

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following content:

```
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./skills_platform.db
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

### Optional Features

- `GET /match/suggestions` - Get AI-based match suggestions (company only)
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
├── requirements.txt
└── README.md
```

## Development

The project uses:

- FastAPI for the web framework
- SQLModel for database ORM
- JWT for authentication
- Pydantic for data validation
- uvicorn for ASGI server

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
