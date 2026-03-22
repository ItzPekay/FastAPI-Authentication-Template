# FastAPI JWT Auth Template

A minimal, production-ready authentication template using FastAPI, JWT tokens, and PostgreSQL.

## Features

- User registration with bcrypt password hashing
- JWT-based login (HS256)
- Protected route guard via FastAPI `Depends`
- PostgreSQL with SQLAlchemy ORM
- Auto-generated Swagger UI at `/docs`

## Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [python-jose](https://github.com/mpdavis/python-jose) — JWT
- [passlib](https://passlib.readthedocs.io/) + bcrypt — password hashing
- [PostgreSQL](https://www.postgresql.org/) via psycopg2

## Getting Started

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd Authentication-Learn
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> Generate a secure secret key with: `openssl rand -hex 32`

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` to explore the API.

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | No | Create a new user |
| POST | `/auth/login` | No | Login and receive a JWT |
| GET | `/users/me` | Yes | Get the current user |

## How to Protect a Route

Add `Depends(get_current_user)` to any route handler:

```python
from app.dependencies import get_current_user
from app.models.user import User

@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}"}
```

The dependency automatically reads the `Authorization: Bearer <token>` header, validates the JWT, and injects the user — no extra setup needed.

## Project Structure

```
app/
├── main.py              # App entry point
├── config.py            # Env var loading
├── database.py          # SQLAlchemy setup
├── dependencies.py      # get_db, get_current_user
├── core/
│   ├── security.py      # Password hashing
│   └── tokens.py        # JWT encode/decode
├── models/user.py       # User ORM model
├── schemas/
│   ├── user.py          # Request schemas
│   └── auth.py          # Token response schema
├── routes/
│   ├── auth.py          # Auth routes
│   └── users.py         # User routes
└── services/
    └── auth_service.py  # Business logic
```
