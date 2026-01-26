from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# Users
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase): # This will be output mode user
    id: int
    role: str
    is_active: bool
    created_at: datetime
    class Config:
        orm_mode = True
