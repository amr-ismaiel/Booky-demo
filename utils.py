from pwdlib import PasswordHash
from datetime import timedelta , datetime , timezone , UTC
from config import Config
import jwt
from uuid import uuid4
import logging

TOKEN_EXPIRY = 3600
REFRESH_TOKEN_EXPIRY = 60 * 60 * 24 * 7  # 7 days

password_hash = PasswordHash.recommended()

def generate_password_hash(password: str) -> str:

    hash = password_hash.hash(password)

    return hash


def verify_password(password: str, hash: str) -> bool:
    try:
        return password_hash.verify(password, hash)
    except Exception:
        return False



def create_access_token(user_data:dict  , expiry:timedelta = None , refresh:bool = False):
    payload = {}

    payload['user'] = user_data
    expire_time = datetime.now() + (expiry if expiry is not None else timedelta(seconds=TOKEN_EXPIRY))
    payload['exp'] = int(expire_time.timestamp())
    payload['iat'] = int(datetime.now(timezone.utc).timestamp())
    payload['jti'] = str(uuid4())

    payload['refresh'] = refresh

    token = jwt.encode(payload , key=Config.JWT_SECRET , algorithm=Config.JWT_ALGORITHM )

    return token


def decode_token(token:str)->dict:
    try:
        token_data = jwt.decode(jwt = token , key=Config.JWT_SECRET , algorithms=Config.JWT_ALGORITHM
        )
        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

