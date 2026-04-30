from datetime import datetime

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from infrastructure.models.book import book

from .schemas import Book_create, Book_update


class Book_service:

    async def get_all_books(self , session:AsyncSession):
        statement = select(book).order_by(desc(book.created_at))
        result = await session.execute(statement)

        return result.scalars().all()


    async def get_book(self , book_id:int , session:AsyncSession):
        statement = select(book).where(book.id == book_id)
        result = await session.execute(statement)

        selected_book =  result.scalars().first()

        return selected_book if selected_book is not None else None



    async def create_book(self , book_data:Book_create, user_id:int, session:AsyncSession):
        book_data_dict = book_data.model_dump()

        new_book = book(**book_data_dict)

        new_book.published_date = datetime.strptime(book_data_dict['published_date'] , '%Y-%m-%d')
        new_book.user_id = user_id
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book) # Get the ID and any DB defaults

        return new_book


    async def update_book(self , book_id:int , book_data:Book_update , session:AsyncSession):
        book_to_update = self .get_book(book_id , session)
        if book_to_update is not None:
            update_book_dict = book_data.model_dump()
            for k , v in update_book_dict.items():
                setattr(book_to_update , k , v)

            await session.commit

            return book_to_update
        return None

    async def delete_book(self , book_id:int , session:AsyncSession):
        book_to_delete = self .get_book(book_id , session)
        if book_to_delete is not None :
            await session.delete(book_to_delete)
            await session.commit
        else:
            return





