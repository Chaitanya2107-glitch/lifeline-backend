# Lifeline Backend

Backend API for the Lifeline emergency response application.

## Tech Stack

- FastAPI
- Supabase
- Railway
- Loguru
- Pydantic

## Setup

```bash
git clone <repository-url>
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file from `.env.example` and add your credentials.

Run the server:

```bash
uvicorn app.main:app --reload
```

## API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

Health Check:

```
http://127.0.0.1:8000/health
```

## Project Structure

See:

```
docs/project-structure.md
```

## Coding Standards

See:

```
docs/coding-conventions.md
```

## ✅ Completed

- User Registration
- User Login
- JWT Authentication
- Protected Routes
- Supabase Integration
- Report Upload (PDF/Image)
- Report Retrieval