from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date
from enum import Enum

class Role(str, Enum):
    STU = "STU"
    ADMIN = "ADMIN"

class UserLoginRequest(BaseModel):
    account_id: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    xquare_id: UUID
    account_id: str
    name: str
    grade: int
    class_num: int
    num: int
    birth_day: date
    device_token: Optional[str] = None
    profile: Optional[str] = None
    role: Role
