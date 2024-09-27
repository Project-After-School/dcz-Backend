from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from fastapi import HTTPException

class NewAdminForm(BaseModel):
  email: EmailStr
  name: str
  password: str

  @field_validator('email', 'name', 'password')
  @classmethod
  def block_empty(cls, v):
    if not v or v.isspace():
      raise HTTPException(status_code=404, detail="필수 항목 입력")
    return v
  
  @field_validator('name')
  @classmethod
  def block_long_name(cls, v):
    if len(v) < 2 or len(v) > 4:
      raise HTTPException(status_code=422, detail="이름은 2자리 이상 4자리 이하로 작성해주세요.")
    return v

  @field_validator('password')
  @classmethod
  def check_password(cls, v):
    if 