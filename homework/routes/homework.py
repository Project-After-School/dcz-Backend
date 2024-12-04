from fastapi import APIRouter, Depends, UploadFile, HTTPException, status, File, Form
# from dotenv import load_dotenv
from sqlalchemy.orm import Session
from homework.database.homework import get_db
from typing import List, Optional
from homework.schemas import homework as homework_schemas
from homework.homework_crud import homework as homework_crud
from admin.models.admin import Teacher
from auth.auth import get_current_teacher
import csv

router = APIRouter(
  prefix="/homework"
)

# @router.post("/get_hws")
# async def get_hws(request: , db: Session = Depends(get_db)):

# @router.get("/")

@router.post("/upload_hw")
async def upload_hw(newhomework: homework_schemas.NewHomework, db: Session = Depends(get_db)):
  try:
    homework_crud.createHomework(newhomework, db)
    return HTTPException(status_code=status.HTTP_200_OK, detail="Homework uploaded successfully")
  except Exception as e:
    print(f"Unexpected Error occured: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error")
  
@router.post("/upload_teacher_file")
async def upload_file(file: UploadFile = File(...), current_teacher: Teacher = Depends(get_current_teacher)):
  try:
    return homework_crud.upload_teacher_file_to_s3(file, current_teacher.id)
  except Exception as e:
    print(f"SERVER ERROR: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected Server Error occured")