from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from user_login.models.user import User
from admin.models.admin import Teacher
from user_login.database import get_db
import os

# JWT 설정
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# FastAPI router
router = APIRouter()

# HTTPBearer 인증 스킴
bearer_scheme = HTTPBearer()

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)  # 디버깅용 출력
        return payload
    except JWTError as e:
        print(f"Token decoding error: {e}")
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
    print("Received token:", token)  # 디버깅용 출력
    
    # 토큰 디코딩
    payload = decode_token(token)
    
    account_id = payload.get("sub")  # sub 필드에서 account_id 가져오기
    
    if account_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 데이터베이스에서 account_id로 유저 조회
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
    print("Received token:", token)  # 디버깅용 출력
    
    # 토큰 디코딩
    payload = decode_token(token)
    
    teacher_id = payload.get("sub")  # sub 필드에서 teacher_id 가져오기
    
    if teacher_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 데이터베이스에서 teacher_id로 교사 조회
    teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
    
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found",
        )
    
    return teacher

# 예시: 인증된 사용자 정보 조회 (학생용)
@router.get("/user/profile")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return {"account_id": current_user.account_id, "role": current_user.role}

# 예시: 인증된 교사 정보 조회
@router.get("/admin/profile")
async def get_teacher_profile(current_teacher: Teacher = Depends(get_current_teacher)):
    return {"teacher_id": current_teacher.teacher_id, "role": current_teacher.role}