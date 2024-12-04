from fastapi import UploadFile, HTTPException, status, File
from sqlalchemy.orm import Session
from typing import List, Optional
from homework.schemas import homework as homework_schemas
from homework.models.homework import Homework
from dotenv import load_dotenv
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
import boto3
import os

load_dotenv()
AWS_S3_ACCESS_KEY = os.getenv("AWS_S3_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_S3_BUCKET_REGION = os.getenv("AWS_S3_BUCKET_REGION")
AWS_S3_PRIVATE_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY")

s3 = boto3.client(
  "s3", aws_access_key_id=AWS_S3_ACCESS_KEY, aws_secret_access_key=AWS_S3_PRIVATE_KEY
)

def upload_teacher_file_to_s3(file: UploadFile, teacher_uuid: str):
  try:
    if not file:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File Not Found")
  
    s3.put_object(Bucket=AWS_S3_BUCKET_NAME, Key=f"dcz/teacher/{teacher_uuid}/")
    s3.upload_fileobj(file.file, AWS_S3_BUCKET_NAME, f"dcz/teacher/{teacher_uuid}/{file.filename}")
    s3_url = f"https://s3.{AWS_S3_BUCKET_REGION}.amazonaws.com/{AWS_S3_BUCKET_NAME}/dcz/teacher/{teacher_uuid}/{file.filename}"
    return s3_url
  except (BotoCoreError, ClientError) as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"failed to upload s3: {e}")

def createHomework(new_homework: homework_schemas.NewHomework, db: Session):
  homework = Homework(
    title = new_homework.title,
    content = new_homework.content,
    submit_detail = new_homework.submit_detail,
    start_date = new_homework.start_date,
    end_date = new_homework.end_date,
    teacher_file_url = new_homework.teacher_file_url,
    selected_grade = new_homework.selected_grade
  )

  db.add(homework)
  db.commit()
  db.refresh(homework)
  return homework

def remove_teacher_file(teacher_uuid: str, filename: str):
  try:
    s3.delete_object(Bucket=AWS_S3_BUCKET_NAME, Key=f"{teacher_uuid}/{filename}")
    return {"message": f"File '{teacher_uuid}/{filename}' deleted successfully from S3 bucket '{AWS_S3_BUCKET_NAME}'"}
  except ClientError as e:
    error_message = e.response['Error']['Message']
    if e.response['Error']['Code'] == "NoSuchKey":
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File '{teacher_uuid}/{filename}' does not exist in bucket {AWS_S3_BUCKET_NAME}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error occured while deleting file: {error_message}")
  except NoCredentialsError as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="AWS credentials not found")
