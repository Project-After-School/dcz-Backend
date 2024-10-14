from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime




class Mypage(BaseModel):
  name: str
  grade: int
  class_num: int
  num: int
  profile: str | None = None
  
  class Config:
    from_attributes = True
  
