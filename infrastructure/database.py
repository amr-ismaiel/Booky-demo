
from datetime import UTC, date, datetime, timezone

from sqlalchemy import DATE, Boolean, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    deferred,
    mapped_column,
    relationship,
    undefer,

)

from config import Config

database_url = Config.DataBase_URL

engine = create_async_engine(

    database_url,
    #connect_args = {'check_same_thread':False},
    echo=True

)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass

async def get_db ()-> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


__all__ = ["DATE", "UTC", "AsyncSession", "Base", "Boolean", "ForeignKey", "Integer", "Mapped", "String", "Text", "date", "datetime", "deferred", "engine", "get_db", "mapped_column", "relationship", "timezone" ,"undefer"]
