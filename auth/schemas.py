from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime, UTC, date


# 3. Key Features of .model_dump()
#
# exclude_unset=True: If you pass this, it will only include fields that the user actually sent in the request (very useful for PATCH/Update operations).
# exclude_none=True: Removes any fields that have a None value.
# Deep Copy: It creates a new dictionary; it doesn't just point to the old data.


class User(BaseModel):
    id: int


class User_create(BaseModel):
    user_name: str = Field(max_length=15)
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=6)
    first_name: str = Field(min_length=1,max_length=20)
    last_name: str = Field(min_length=1,max_length=20)



class User_response(BaseModel):
    id: int
    user_name: str
    email: str
    # password_hash:str = deferred( mapped_column())
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class User_login(BaseModel):
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=6)

