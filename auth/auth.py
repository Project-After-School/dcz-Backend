from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from user_login.models.user import User
from admin.models.admin import Teacher
from user_login.database import get_db
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

router = APIRouter()

bearer_scheme = HTTPBearer()

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    
    payload = decode_token(token)
    
    account_id = payload.get("sub")  
    
    if account_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.account_id == account_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user

async def get_current_teacher(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    
    
    payload = decode_token(token)
    
    teacher_id = payload.get("sub")  
    
    if teacher_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
    
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found",
        )
    
    return teacher

@router.get("/user/profile")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return {"account_id": current_user.account_id, "role": current_user.role}

@router.get("/admin/profile")
async def get_teacher_profile(current_teacher: Teacher = Depends(get_current_teacher)):
    return {"teacher_id": current_teacher.teacher_id, "role": current_teacher.role}