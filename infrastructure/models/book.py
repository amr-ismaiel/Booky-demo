import sqlalchemy.dialects.postgresql as pg

from typing import TYPE_CHECKING

from ..database import (
    DATE,
    UTC,
    Base,
    Integer,
    Mapped,
    String,
    date,
    datetime,
    mapped_column,
    ForeignKey,
    relationship
)

if TYPE_CHECKING:
    # هذا الاستيراد يتم فقط من أجل الـ Type Hinting ولا يسبب Circular Import
    from .user import user


class book (Base):
    __tablename__ = 'books'

    id:Mapped[int] = mapped_column(Integer,primary_key=True , index=True)
    title:Mapped[str] = mapped_column(String(100),nullable=False)
    author:Mapped[str] = mapped_column(String(50),nullable=False)
    publisher:Mapped[str] = mapped_column(String(100),nullable=False)
    published_date:Mapped[date | None] = mapped_column(DATE)
    page_count:Mapped[int] = mapped_column(Integer)
    language:Mapped[str] = mapped_column(String(50))
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id') ,nullable=False , index=True)
    created_at:Mapped[datetime] = mapped_column(pg.TIMESTAMP(timezone=True) , default=lambda:datetime.now(UTC))
    updated_at:Mapped[datetime] = mapped_column(pg.TIMESTAMP(timezone=True) , default=lambda:datetime.now(UTC))


    creator: Mapped['user'] = relationship('user',back_populates="books")



