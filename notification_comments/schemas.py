from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class CommentsBase(BaseModel):
  content : str
  
class CreateComments(CommentsBase):
  pass

class Comments(CommentsBase):
  id : int
  author_id : UUID
  notification_id : int
  date : datetime
  
  class Config:
    from_attributes = True
  