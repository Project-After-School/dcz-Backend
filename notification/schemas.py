from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from uuid import UUID
from datetime import datetime



class NotificationBase(BaseModel):
    title: str
    content: str
    grade: List[str]  
    class_num: List[str]  


class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    author_id: UUID
    author_name: str
    date: datetime
  
    class Config:
        from_attributes = True

class NotificationSimple(BaseModel):
    title: str
    date: datetime
    id: int
     
    class Config:
        from_attributes = True
       
class NotificationUpdate(NotificationBase):
    pass

