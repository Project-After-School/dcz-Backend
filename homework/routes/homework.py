from fastapi import APIRouter, Depends, UploadFile, HTTPException, status, File, Form
# from dotenv import load_dotenv
from sqlalchemy.orm import Session
from homework.database.homework import get_db
from typing import List, Optional
from homework.schemas import homework as homework_schemas
from homework.homework_crud import homework as homework_crud
import csv

router = APIRouter(
  prefix="/homework"
)

# @router.post("/get_hws")
# async def get_hws(request: , db: Session = Depends(get_db)):

@router.post("/upload_hw")
def upload_hw(newhomework: homework_schemas.NewHomework, db: Session = Depends(get_db), files: Optional[List[UploadFile]] = File([])):
  try:
    print(files)
    homework_crud.createHomework(newhomework, db, files)
    return HTTPException(status_code=status.HTTP_200_OK, detail="Homework uploaded successfully")
  except Exception as e:
    print(f"Unexpected Error occured: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error")