from pydantic import BaseModel, EmailStr, field_validator, ValidationError, constr
from admin.models.admin import SchoolClass
from fastapi import HTTPException

class Token(BaseModel):
  access_token: str
  token_type: str

class NewAdminForm(BaseModel):
  teacher_id: str
  email: EmailStr
  name: constr(min_length=2, max_length=4)
  major: str = None
  password: constr(min_length=8)
  teacher_class: SchoolClass

  @field_validator('teacher_id', 'name', 'password')
  @classmethod
  def block_empty(cls, v):
    if not v or v.isspace():
      raise HTTPException(status_code=404, detail="필수 항목 입력")
    return v