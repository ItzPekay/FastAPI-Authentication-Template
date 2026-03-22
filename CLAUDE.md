# Authentication-Learn

A FastAPI-based authentication system with JWT tokens and PostgreSQL.

## Project Structure

```
app/
├── main.py              # FastAPI app, router registration, table creation
├── dependencies.py      # get_db, get_current_user (JWT guard)
├── config.py            # Loads env vars via python-dotenv
├── database.py          # SQLAlchemy engine, SessionLocal, Base
├── core/
│   ├── security.py      # Password hashing/verification (passlib/bcrypt)
│   └── tokens.py        # JWT encode/decode (python-jose)
├── models/
│   └── user.py          # User ORM: id, username, password (table name "Users")
├── schemas/
│   ├── user.py          # UserCreate and UserLogin Pydantic schemas
│   └── auth.py          # Token response schema
├── routes/
│   ├── auth.py          # POST /auth/register, POST /auth/login
│   └── users.py         # GET /users/me (protected)
└── services/
    ├── auth_service.py  # register() and login() logic
    └── user_service.py  # empty — extend as needed
```

## What's Working

- `POST /auth/register` — creates a user with a bcrypt-hashed password
- `POST /auth/login` — verifies credentials, returns a signed JWT
- `GET /users/me` — returns the current authenticated user
- `get_current_user()` dependency — decodes and validates JWT, injects user into routes
- Database table auto-created on startup via `Base.metadata.create_all`

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
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Key Notes

- All imports inside `app/` use relative imports (e.g. `from .database import SessionLocal`).
- Run with `uvicorn app.main:app` from the project root.
- JWT tokens use the `sub` claim to store the user ID as a string.
- The User table name is `"Users"` (capital U) — keep consistent when writing queries.
- Protect any route by adding `current_user: User = Depends(get_current_user)` as a parameter.
