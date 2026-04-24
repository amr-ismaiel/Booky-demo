# from .book_data import books

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from infrastructure.database import AsyncSession, get_db

from .schemas import Book, Book_create, Book_update
from .service import Book_service

from typing import Annotated
from auth.dependencies import Access_token_bearer , HTTPBearer

book_router = APIRouter()
book_service = Book_service()

DBSession = Annotated[AsyncSession, Depends(get_db)]

access_token_bearer = Annotated[HTTPBearer ,Depends(Access_token_bearer())]
#access_token_bearer = Access_token_bearer()


@book_router.get("", response_model=list[Book])
async def get_all_books(session: DBSession , user_details : access_token_bearer):

    books = await book_service.get_all_books(session)
    return books


@book_router.post("", status_code=status.HTTP_201_CREATED)
async def create_book(book_data: Book_create, session: DBSession):
    new_book = await book_service.create_book(book_data, session)
    return new_book


@book_router.get("/{book_id}")
async def get_book(book_id: int, session: DBSession):
    book = await book_service.get_book(book_id, session)

    if book:
        return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="The Book Not Found"
    )


@book_router.patch("/{book_id}")
async def update_book(
    book_id: int, book_update_data: Book_update, session: DBSession
) -> dict:
    updated_book = await book_service.update_book(book_id, book_update_data, session)

    if updated_book:
        return updated_book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="The Book Not Found"
    )


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, session: DBSession):
    book_to_delete = await book_service.delete_book(book_id, session)

    if book_to_delete:
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")
