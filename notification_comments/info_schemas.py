from pydantic import BaseModel
from typing import Optional, Union
from uuid import UUID
from datetime import datetime

class User(BaseModel):
    id: UUID
    name: str  

    class Config:
        from_attributes = True

class Teacher(BaseModel):
    id: UUID
    teacher_name: str  
    name: str  

    class Config:
        from_attributes = True
