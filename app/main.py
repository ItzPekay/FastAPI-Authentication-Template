from fastapi import FastAPI
from .routes import auth, users
from .database import Base, engine
from .models import user, refresh_token  # ensures models are registered with Base before create_all
from fastapi.middleware.cors import CORSMiddleware
from .config import ALLOWED_ORIGINS

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Learn Auth API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)



app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])