from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status
from fastapi.security.http import HTTPAuthorizationCredentials
from utils import decode_token

class Access_token_bearer(HTTPBearer):
    def __init__(self ,auto_error=True):
        super().__init__(auto_error=auto_error)


    async def __call__(self , request:Request)->HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        if creds is not None and not self.token_valid(creds.credentials):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )






    def token_valid(self , token:str) -> bool:
        try:
            decode_token(token)
            return True
        except Exception: # Broad exception to catch any decoding issues from utils.decode_token
            return False
