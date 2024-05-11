from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, PastDate

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)

class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class EmailModel(BaseModel):
    email: EmailStr = Field(max_length=25)


class EmailResponse(EmailModel):
    id: int

    class Config:
        orm_mode = True

class RequestEmail(BaseModel):
    email: EmailStr

class ContactBase(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=100)
    birthday: PastDate
    description: str = Field(max_length=250)


class ContactModel(ContactBase):
    emails: List[int]


class ContactResponse(ContactBase):
    id: int
    emails: List[EmailResponse]

    class Config:
        orm_mode = True
