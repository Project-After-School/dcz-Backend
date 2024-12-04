from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import EmailStr
from admin.database.admin import Settings
from admin.models import admin as admin_models
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from admin.admin_crud.admin_crud import get_admin
import os
import jwt

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM" , "HS256")
ACCESS_TOKEN_EXPIRES_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES")
# ACCESS_TOKEN_EXPIRES_MINUTES = 1440

token_url = OAuth2PasswordBearer(tokenUrl="/admin/login")

# settings = Settings()

# def create_access_token(teacher: EmailStr, expirationtime: int):
#   payload = {
#     'teacher': teacher,
#     'expires': expirationtime
#   }

def create_access_token(data: dict, expires_delta: timedelta):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=99)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  decoded_jwt = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=ALGORITHM)
  print("-------")
  print(decoded_jwt)
  print(encoded_jwt)

  return encoded_jwt

def get_admin(token: str = Depends(token_url), db: Session = Depends(get_admin)):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    if not payload:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payload(data) not found", headers={"Content-Type": "application/json"})

    admin_id = str(payload.get("sub"))

    if not admin_id:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin ID not found. (ID could be wrong)", headers={"WWW-Authenticate": "Bearer"})
    
    admin = db.query(admin_models.Teacher).filter(admin_models.Teacher.teacher_id == admin_id).first()

    if admin == None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="admin data not found.", headers={"WWW-Authenticate": "Bearer"})
    
    return admin
  
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired.", headers={"WWW-Authenticate": "Bearer"})
  except jwt.PyJWTError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Token", headers={"WWW-Authenticate": "Bearer"})