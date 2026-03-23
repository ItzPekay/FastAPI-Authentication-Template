# Authentication-Learn

A FastAPI-based authentication system with JWT tokens, refresh token rotation, rate limiting, CORS, and PostgreSQL.

## Project Structure

```
app/
├── main.py              # FastAPI app, middleware (CORS), router registration, table creation
├── dependencies.py      # get_db, get_current_user (JWT bearer guard)
├── config.py            # Loads env vars via python-dotenv
├── database.py          # SQLAlchemy engine, SessionLocal, Base
├── core/
│   ├── security.py      # Password hashing/verification (passlib/bcrypt)
│   ├── tokens.py        # JWT encode/decode (python-jose), opaque refresh token generation
│   └── limiter.py       # Custom in-memory rate limiter (RateLimiter class)
├── models/
│   ├── user.py          # User ORM: id, username, password (table name "Users")
│   └── refresh_token.py # RefreshToken ORM: id, token, user_id, expires_at, revoked
├── schemas/
│   ├── user.py          # UserCreate, UserLogin, UserResponse Pydantic schemas
│   └── auth.py          # Token and RefreshRequest schemas
├── routes/
│   ├── auth.py          # POST /auth/register, /auth/login, /auth/refresh, /auth/logout
│   └── users.py         # GET /users/me (protected)
└── services/
    ├── auth_service.py  # register(), login(), refresh(), logout() logic
    └── user_service.py  # empty — extend as needed
```

## What's Working

- `POST /auth/register` — creates a user with a bcrypt-hashed password, rate limited to 3/min
- `POST /auth/login` — verifies credentials, returns access token + refresh token, rate limited to 5/min
- `POST /auth/refresh` — validates refresh token, rotates it, returns new access + refresh token
- `POST /auth/logout` — revokes the refresh token
- `GET /users/me` — returns the current authenticated user (JWT protected)
- `get_current_user()` dependency — decodes and validates JWT, injects user into routes
- CORS middleware — configurable allowed origins via env var
- Rate limiting — custom in-memory limiter, no external dependencies
- Database tables auto-created on startup via `Base.metadata.create_all`

## Running the App

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment Variables (.env)

```
DATABASE_URL=postgresql://user:password@localhost:5433/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

## Key Notes

- All imports inside `app/` use relative imports (e.g. `from .database import SessionLocal`).
- Run with `uvicorn app.main:app` from the project root.
- JWT access tokens use the `sub` claim to store the user ID as a string.
- Refresh tokens are opaque (`secrets.token_urlsafe(32)`), stored in the DB, and rotated on every use.
- A used or expired refresh token is rejected — only the latest issued token is valid.
- The User table name is `"Users"` (capital U) — keep consistent when writing queries.
- Protect any route by adding `current_user: User = Depends(get_current_user)` as a parameter.
- Rate limiter is in-memory — resets on server restart. For multi-server deployments, swap for Redis-backed limiting.
- `refresh_tokens` table accumulates expired rows over time — add a periodic cleanup job in production.
