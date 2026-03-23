# FastAPI JWT Auth

A full-featured authentication backend using FastAPI, JWT access tokens, refresh token rotation, rate limiting, CORS, and PostgreSQL.

## Features

- User registration with bcrypt password hashing
- JWT login (HS256) with short-lived access tokens
- Opaque refresh tokens with rotation on every use
- Revocation-based logout
- Protected route guard via FastAPI `Depends`
- Custom in-memory rate limiter (no Redis required)
- CORS middleware with configurable origins
- PostgreSQL with SQLAlchemy ORM
- Alembic for database migrations
- Auto-generated Swagger UI at `/docs`

## Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/) + [Alembic](https://alembic.sqlalchemy.org/)
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
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

> Generate a secure secret key with: `openssl rand -hex 32`

### 5. Run migrations

```bash
alembic upgrade head
```

### 6. Run the server

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` to explore the API.

## API Endpoints

| Method | Endpoint | Auth | Rate Limit | Description |
|--------|----------|------|------------|-------------|
| POST | `/auth/register` | No | 3/min | Create a new user |
| POST | `/auth/login` | No | 5/min | Login and receive access + refresh tokens |
| POST | `/auth/refresh` | No | — | Rotate refresh token, get new access token |
| POST | `/auth/logout` | No | — | Revoke the refresh token |
| GET | `/users/me` | Yes | — | Get the current authenticated user |
| GET | `/health` | No | — | Health check |

## Token Flow

1. **Login** → returns `access_token` (15 min) + `refresh_token` (7 days)
2. **Authenticated requests** → send `Authorization: Bearer <access_token>` header
3. **When access token expires** → call `/auth/refresh` with your `refresh_token` to get a new pair
4. **Logout** → call `/auth/logout` with your `refresh_token` to revoke it

Refresh tokens are rotated on every use — the old token is invalidated immediately.

## How to Protect a Route

Add `Depends(get_current_user)` to any route handler:

```python
from app.dependencies import get_current_user
from app.models.user import User

@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}"}
```

The dependency reads the `Authorization: Bearer <token>` header, validates the JWT, and injects the user.

## Project Structure

```
app/
├── main.py              # FastAPI app, CORS middleware, router registration
├── config.py            # Env var loading via python-dotenv
├── database.py          # SQLAlchemy engine, SessionLocal, Base
├── dependencies.py      # get_db, get_current_user (JWT bearer guard)
├── alembic/             # Database migration scripts
├── core/
│   ├── security.py      # Password hashing/verification
│   ├── tokens.py        # JWT encode/decode, refresh token generation
│   └── limiter.py       # Custom in-memory rate limiter
├── models/
│   ├── user.py          # User ORM model
│   └── refresh_token.py # RefreshToken ORM model
├── schemas/
│   ├── user.py          # UserCreate, UserLogin, UserResponse
│   └── auth.py          # Token, RefreshRequest schemas
├── routes/
│   ├── auth.py          # Auth routes
│   └── users.py         # User routes
└── services/
    └── auth_service.py  # register, login, refresh, logout logic
```

## Notes

- Rate limiter is in-memory — resets on server restart. Swap for a Redis-backed solution in multi-server deployments.
- The `refresh_tokens` table accumulates expired rows over time — add a periodic cleanup job in production.
- The `Users` table name uses a capital U — keep consistent when writing raw queries.
