from pydantic import BaseModel
from datetime import datetime


class NewsBase(BaseModel):
    title: str
    content: str
    publish_date: datetime


class NewsCreate(NewsBase):
    pass


class News(NewsBase):
    id: int
    author: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    is_admin: bool
    news: list[News] = []

    class Config:
        orm_mode = True
