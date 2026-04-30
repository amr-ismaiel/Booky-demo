import sqlalchemy.dialects.postgresql as pg

from typing import TYPE_CHECKING


from ..database import (
    UTC,
    Base,
    Boolean,
    Integer,
    Mapped,
    String,
    datetime,
    deferred,
    mapped_column,
    ForeignKey,
    relationship
)

if TYPE_CHECKING:
    # هذا الاستيراد يتم فقط من أجل الـ Type Hinting ولا يسبب Circular Import
    from .book import book

class user(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = deferred(mapped_column(String, nullable=False))
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    role:Mapped[str] = mapped_column(String(10),nullable=False,server_default='user')
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(UTC)
    )

    books: Mapped[list['book']] = relationship('book',back_populates="creator")
