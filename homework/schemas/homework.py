from pydantic import BaseModel
from fastapi import HTTPException
from datetime import datetime
from typing import List

class NewHomework(BaseModel):
  # homework_id: int
  title: str
  content: str
  submit_detail: str
  start_date: datetime
  end_date: datetime
  teacher_file_url: str = None
  selected_grade: str