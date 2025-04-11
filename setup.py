from setuptools import setup, find_packages

setup(
    name="massai-hackathon",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.110.0",
        "uvicorn==0.27.1",
        "sqlmodel==0.0.14",
        "pydantic==2.6.1",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.9",
        "python-dotenv==1.0.1",
        "email-validator==2.1.0.post1"
    ],
) 