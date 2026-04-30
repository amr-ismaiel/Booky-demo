from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from books.router import book_router
from auth.router import auth_router
from infrastructure.database import Base, engine


@asynccontextmanager
async def life_span(app: FastAPI):
    async with engine.begin() as conn:
        print("hello database engin start")
        #await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()


app = FastAPI()

app.include_router(book_router, prefix="/books" , tags=['Books'])
app.include_router(auth_router, prefix="/user" , tags=['Users'])
