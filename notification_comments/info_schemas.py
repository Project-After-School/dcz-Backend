from pydantic import BaseModel
from typing import Optional, Union
from uuid import UUID
from datetime import datetime

# User 모델 (필요한 모든 필드 포함)
class User(BaseModel):
    id: UUID
    name: str  # name 필드가 존재해야 함

    class Config:
        from_attributes = True

# Teacher 모델 (필요한 모든 필드 포함)
class Teacher(BaseModel):
    id: UUID
    teacher_name: str  # teacher_name 필드가 존재하지만, name도 포함시키기
    name: str  # name 필드가 추가되어야 함

    class Config:
        from_attributes = True
