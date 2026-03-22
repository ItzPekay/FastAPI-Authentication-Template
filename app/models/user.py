from sqlalchemy import Column, String, Integer
from ..database import Base

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

