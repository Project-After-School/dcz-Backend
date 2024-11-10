from fastapi import UploadFile, HTTPException, status, File
from sqlalchemy.orm import Session
from typing import List, Optional
from homework.schemas import homework as homework_schemas
from homework.models.homework import Homework
from dotenv import load_dotenv
from botocore.exceptions import BotoCoreError, ClientError
import boto3
import os

load_dotenv()
AWS_S3_ACCESS_KEY = os.getenv("AWS_S3_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_S3_BUCKET_REGION = os.getenv("AWS_S3_BUCKET_REGION")
AWS_S3_PRIVATE_KEY = os.getenv("AWS_S3_PRIVATE_KEY")

s3 = boto3.client(
  "s3", aws_access_key_id=AWS_S3_ACCESS_KEY, aws_secret_access_key=AWS_S3_PRIVATE_KEY
)

def upload_file_to_s3(file: UploadFile):
  try:
    s3.upload_fileobj(file.file, AWS_S3_BUCKET_NAME, f"dcz/{file.filename}")
    s3_url = f"https://s3.{AWS_S3_BUCKET_REGION}.amazonaws.com/{AWS_S3_BUCKET_NAME}/dcz/{file.filename}"
    return s3_url
  except (BotoCoreError, ClientError) as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"failed to upload s3: {e}")

def createHomework(new_homework: homework_schemas.NewHomework, db: Session, files: Optional[List[UploadFile]] = None):
  if files:
    teacher_file_urls = [upload_file_to_s3(file) for file in files]
    teacher_file_url_str = ";".join(teacher_file_urls)
  else:
    teacher_file_url_str = ""
  
  homework = Homework(
    title = new_homework.title,
    content = new_homework.content,
    submit_detail = new_homework.submit_detail,
    startdate = new_homework.start_date,
    enddate = new_homework.end_date,
    teacher_file_url = teacher_file_url_str,
    selected_grade = new_homework.selected_grade
  )

  db.add(homework)
  db.commit()
  db.refresh(homework)
  return homework