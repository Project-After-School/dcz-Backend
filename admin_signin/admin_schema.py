from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from fastapi import HTTPException

class NewAdminForm(BaseModel):
  email: EmailStr
  name: str
  major: str
  password: str

  @field_validator('email', 'major', 'name', 'password')
  @classmethod
  def block_empty(cls, v):
    if not v or v.isspace():
      raise HTTPException(status_code=404, detail="필수 항목 입력")
    return v
  
  @field_validator('name')
  @classmethod
  def block_long_name(cls, v):
    if len(v) < 2 or len(v) > 4:
      raise HTTPException(status_code=400, detail="이름은 2자리 이상 4자리 이하로 작성해주세요.")
    return v

  @field_validator('password')
  @classmethod
  def check_password(cls, v):
    if len(v) < 8:
      raise HTTPException(status_code=400, detail='비밀번호는 8자리 이상 작성해주세요.')