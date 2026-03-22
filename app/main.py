from fastapi import FastAPI
from .routes import auth, users
from .database import Base, engine
from .models import user  # ensures User model is registered with Base before create_all

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Learn Auth API")

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])