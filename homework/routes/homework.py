from fastapi import APIRouter, Depends, UploadFile, HTTPException, status, File, Form
# from dotenv import load_dotenv
from sqlalchemy.orm import Session, joinedload
from homework.database.homework import get_db
from typing import List, Optional
from homework.schemas import homework as homework_schemas
from homework.homework_crud import homework as homework_crud
from homework.models.homework import Homework, User, Teacher
from auth.auth import get_current_teacher, get_current_user
from io import BytesIO
import csv

router = APIRouter(
  prefix="/homework"
)

# @router.post("/get_hws")
# async def get_hws(request: , db: Session = Depends(get_db)):

@router.get("/alladmin")
async def check_all_homeworks_admin(current_teacher: Teacher = Depends(get_current_teacher), db: Session = Depends(get_db)):
  try:
    homeworks = db.query(Homework).filter(Homework.author_id == current_teacher.id).all()
    homeworks_all = homework_crud.check_all_homeworks_admin(homeworks)
    if not homeworks_all:
      return HTTPException(status_code=status.HTTP_200_OK, detail="등록된 과제가 없습니다.")
    return homeworks_all
  
  except AttributeError as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"AttributeError occurred:{e}")
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"ValueError occurred: {e}")
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error occurred: {e}")

# @router.get("/detailadmin")
# async def check_homewrk_admin(homework_id: int, current_teacher: Teacher = Depends(get_current_teacher), db: Session = Depends(get_db)):
#   try:
#     homework = db.query(Homework).filter(Homework.homework_id == homework_id).first()
#     if not homework:
#       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unexist homework id given")
    

@router.get("/alluser")
async def check_all_homeworks_user(selected_subject: str, current_student: User = Depends(get_current_user), db: Session = Depends(get_db)):
  try:
    user_class = f"{str(current_student.grade)}-{current_student.class_num}"
    homeworks = db.query(Homework).options(joinedload(Homework.author)).filter(Homework.selected_grade.contains([user_class])).filter(Homework.author.has(major=selected_subject)).all()
    homeworks_all_user = homework_crud.check_all_homeworks_user(homeworks)
    if not homeworks_all_user:
      return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="등록된 과제가 없습니다.")
    return homeworks_all_user
  
  except AttributeError as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"AttributeError occurred: {e}")
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Value Error occurred: {e}")
  except Exception as e:
    HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Unexpected error occurred in "/alluser": {e}')

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
    file_content = await file.read()
    file_stream = BytesIO(file_content)
    file_format = file.filename.split(".")[-1]

    return homework_crud.upload_teacher_file_to_s3(file, current_teacher.id, file_stream, file_format)
  except Exception as e:
    print(f"SERVER ERROR: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected Server Error occured")