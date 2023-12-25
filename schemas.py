from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    published: bool

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
