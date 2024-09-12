from pydantic import BaseModel, Field

class UserBase(BaseModel):
    email: str
    username: str = Field(..., min_length=2, description="사용자 이름은 작성해주세요")

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str