from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status
from fastapi.security.http import HTTPAuthorizationCredentials
from utils import decode_token
from infrastructure.redis import token_in_blocklist
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

