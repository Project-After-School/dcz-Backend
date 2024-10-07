from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class NotificationBase(BaseModel):
    title: str
    content: str
    
class NotificationCreate(NotificationBase):
     pass

class Notification(NotificationBase):
  id : int
  author_id: UUID
  author_name: str
  date: datetime
  
  class Config:
    from_attributes = True
    
class NotificationUpdate(NotificationBase):
    pass