from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at : datetime
    updated_at : datetime




class Book_create(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str

    page_count: int
    language: str
    model_config = ConfigDict(from_attributes=True)


class Book_update(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str



