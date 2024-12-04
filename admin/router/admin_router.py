from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from admin.database.admin import get_db
from admin.schemas import admin as admin_schemas
from admin.exceptions import UserNotFoundException, PasswordNotMatch
from datetime import timedelta, timezone
from dotenv import load_dotenv
from admin.auth.admin import create_access_token
from pydantic import Json
import admin.schemas.admin as admin
import admin.admin_crud.admin_crud as admin_crud
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))

router = APIRouter(
  prefix="/admin"
)

@router.post('/signup')
async def signup(new_teacher: admin.NewAdminForm, db: Session = Depends(get_db)):
  try:
    teacher = admin_crud.get_admin(new_teacher.email, db)

    if teacher:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')

    admin_crud.create_admin(new_teacher, db)

    return HTTPException(status_code=status.HTTP_200_OK, detail="Singup Succeed")
  except UserNotFoundException:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
  except PasswordNotMatch:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password does not match")
  except Exception as e:
    print(f"Unexpected Error: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.post('/login')
async def login(response: Response, login_form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  user = admin_crud.get_admin(login_form.username, db)

  if not user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user or password")
  
  res = admin_crud.verify_password(login_form.password, user.hashed_pw)

  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(data={"sub": user.teacher_id}, expires_delta=access_token_expires)

  response.set_cookie(key="access_token", value=access_token, expires=access_token_expires, httponly=True)

  if not res:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user or password")
  
  return admin_schemas.Token(access_token=access_token, token_type="bearer")

@router.get("/logout")
async def logout(response: Response, request: Request):
  access_token = request.cookies.get("access_token")

  response.delete_cookie(key="access_token")

  return HTTPException(status_code=status.HTTP_200_OK, detail="Logout Succeed")