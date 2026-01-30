from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# Users
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserAdmin(UserCreate):
    role: str

class UserOut(UserBase): # This will be output mode user
    id: int
    role: str
    is_active: bool
    created_at: datetime
    class Config:
        orm_mode = True


class UserPatch(BaseModel):
    is_active: Optional[bool] = None
    role: Optional[str] = None

    class Config:
        orm_mode = True