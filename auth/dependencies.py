from __future__ import annotations
from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status , Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from utils import decode_token
from typing import Annotated , List
from infrastructure.database import get_db, AsyncSession
from auth.service import User_service
from infrastructure.redis import token_in_blocklist
from infrastructure.models.auth import user

user_service = User_service()
DBSession = Annotated[AsyncSession, Depends(get_db)]




class Token_bearer(HTTPBearer):

    def __init__(self ,auto_error=True):
        super().__init__(auto_error=auto_error)


    async def __call__(self , request:Request)->HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        print(creds.scheme)
        print(creds.credentials)
        token = creds.credentials

        token_data = decode_token(token)

        if creds is not None and not self.token_valid(creds.credentials):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This Token is invalid or has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )

        self.verify_token_data(token_data)


        return token_data






    def token_valid(self , token:str) -> bool:
        try:
            decode_token(token)
            return True
        except Exception: # Broad exception to catch any decoding issues from utils.decode_token
            return False

    def verify_token_data(self , token_data):
        raise NotImplementedError('Please Override This Method In Child Classes')



class Access_token_bearer(Token_bearer):

    def verify_token_data(self , token_data:dict)->None:
        if token_data and token_data['refresh']:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Please Provide an Access Token",
                    headers={"WWW-Authenticate": "Bearer"},
                )

class Refresh_token_bearer(Token_bearer):

    def verify_token_data(self , token_data:dict)->None:
        if token_data and not token_data['refresh']:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Please Provide a Refresh Token",
                    headers={"WWW-Authenticate": "Bearer"},
                )

Token_Details = Annotated[HTTPBearer , Depends(Access_token_bearer())]

async def get_current_user(token_details:Token_Details , session:DBSession):
    user_email = token_details['user']['email']
    user = await user_service.get_user_by_email(user_email,session)

    return user

Current_user = Annotated[user,Depends(get_current_user)]


class Role_checker:
    def __init__(self,allowed_roles:List[str]):

        self.allowed_roles = allowed_roles

    def __call__(self,current_user:Current_user):
        if current_user.role in self.allowed_roles:
            return True
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail='You are not allowed to perform this action')
