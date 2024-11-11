from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Union

class User(BaseModel):
    id: UUID

    class Config:
        from_attributes = True

class Teacher(BaseModel):
    id: UUID

    class Config:
        from_attributes = True

class NotificationComments(BaseModel):
    id: int
    content: str
    date: datetime
    author_id: UUID  
    notification_id: int
    author_type: str

    class Config:
        from_attributes = True

class CreateComments(BaseModel):
    content: str  

    class Config:
        from_attributes = True
        
class Notificationget(BaseModel):
    id: int
    content: str
    date: datetime
    author_id: UUID  
    notification_id: int
    author_type: str
    author_name: str

    class Config:
        from_attributes = True