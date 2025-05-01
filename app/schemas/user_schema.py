from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(None, max_length=50)
    email: EmailStr
    phone_no: Optional[str] = Field(None, max_length=20)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=50)

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone_no: Optional[str] = Field(None, max_length=20)
    addresses: Optional[List[str]] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    addresses: List[str] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None

# class AddressBase(BaseModel):
#     address: str
#     is_default: bool = False

# class AddressCreate(AddressBase):
#     pass

# class AddressUpdate(AddressBase):
#     address: Optional[str] = None

# class Address(AddressBase):
#     id: int
#     user_id: int

#     class Config:
#         orm_mode = True