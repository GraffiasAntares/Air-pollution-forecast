from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegistration(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[str] = 'user'

class User(BaseModel):
    email: str
    password: str
    role: str

class Message(BaseModel):
    message: str