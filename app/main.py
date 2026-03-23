from fastapi import FastAPI
from .routes import auth, users
from fastapi.middleware.cors import CORSMiddleware
from .config import ALLOWED_ORIGINS


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

@app.get("/health")
def health():
    return {"status" : "ok"}