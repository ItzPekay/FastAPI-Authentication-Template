from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=128)

class UserLogin(UserCreate):
    pass

class UserResponse(BaseModel):
    id: int
    username: str