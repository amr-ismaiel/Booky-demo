from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from .schemas import User_create, User_response , User_login
from .service import User_service
from infrastructure.database import get_db, AsyncSession
from typing import Annotated
from utils import create_access_token , decode_token , verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse


auth_router = APIRouter()
user_service = User_service()
DBSession = Annotated[AsyncSession, Depends(get_db)]



@auth_router.post(
    "/signup", response_model=User_response, status_code=status.HTTP_201_CREATED
)
async def create_user_account(user_data: User_create ,session:DBSession):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exist",
        )

    new_user = await user_service.user_create(user_data, session)

    return new_user


@auth_router.post("/signin")
async def login_user(login_data:User_login , session:DBSession):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email , session)

    if user is not None :
        password_valid = verify_password(password , user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_id':str(user.id)
                    }
                )
            refresh_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_id':str(user.id)
                    },
                refresh=True,
                expiry=timedelta(days=2)
                )
            return JSONResponse(
                content={
                    'message':'Login Success',
                    'access_token':access_token,
                    'refresh_token':refresh_token,
                    'user':{
                        'email':user.email,
                        'id':str(user.id)
                        }

                    }
                )
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail='Invalid Email Or Password')
