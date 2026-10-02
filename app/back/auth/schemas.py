import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    email: str
    role: str


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    role: str

