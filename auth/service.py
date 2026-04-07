
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from infrastructure.models.auth import user
from utils import generate_password_hash

from .schemas import User_create
from sqlalchemy.orm import undefer


class User_service:

    async def get_user_by_email(self , email:str , session:AsyncSession):
        statement = select(user).where(user.email == email).options(undefer(user.password_hash))
        result = await session.execute(statement)

        selected_user = result.scalars().first()

        return selected_user



    async def user_exists(self , email:str , session:AsyncSession):
        user_exist_check = await self.get_user_by_email(email , session)
        return True if user_exist_check is not None else False



    async def user_create (self , user_data:User_create , session:AsyncSession):
        user_data_dict = user_data.model_dump()
        print('user data received')
        hashed_pwd = generate_password_hash(user_data_dict['password'])
        print(user_data_dict['password'])
        print(hashed_pwd)


        user_data_dict['password_hash'] = user_data_dict.pop('password')
        user_data_dict['password_hash'] = hashed_pwd
        new_user = user(**user_data_dict )


        session.add(new_user)

        await session.commit()
        await session.refresh(new_user)

        return new_user
