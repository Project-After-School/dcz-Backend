from fastapi import UploadFile, HTTPException, status, File
from sqlalchemy.orm import Session
from typing import List, Optional
from homework.schemas import homework as homework_schemas
from homework.models.homework import Homework
from dotenv import load_dotenv
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
from datetime import datetime, timezone
from io import BytesIO
from fpdf import FPDF
from PIL import Image
from PyPDF2 import PdfReader
import boto3
import os
import pyhwp

load_dotenv()
AWS_S3_ACCESS_KEY = os.getenv("AWS_S3_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_S3_BUCKET_REGION = os.getenv("AWS_S3_BUCKET_REGION")
AWS_S3_PRIVATE_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY")

s3 = boto3.client(
  "s3", aws_access_key_id=AWS_S3_ACCESS_KEY, aws_secret_access_key=AWS_S3_PRIVATE_KEY
)

def extract_hwp_text(hwp_stream):
  doc = pyhwp.document.load(hwp_stream)
  text = ''.join(section.text for section in doc.sections)
  return text

def upload_teacher_file_to_s3(file: UploadFile, teacher_uuid: str):
  try:
    if not file:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File Not Found")

    # if file_format == "txt":
    #   text = file_stream.read().decode("utf-8")
    #   pdf = FPDF()
    #   pdf.add_page()
    #   pdf.set_font("Arial", size=12)
    #   pdf.multi_cell(0, 10, text)

    # elif file_format == "jpg" or file_format == "png":
    #   image = Image.open(file_stream)
    #   pdf = BytesIO()
    #   image.save(pdf, "PDF", resolution=100.0)
    #   pdf.seek(0)

    # elif file_format == "hwp":
    #   extracted_text = extract_hwp_text(file_stream)

    #   pdf = FPDF()
    #   pdf.add_page()
    #   pdf.set_font("Arial", size=12)
    #   for line in extracted_text.split("\n"):
    #     pdf.cell(200, 10, txt=line, ln=True)

    # else:
    #   reader = PdfReader(file_stream)
    #   pdf = [page.extract_text() for page in reader.pages]

    # pdf_stream = BytesIO()
    # pdf.output(pdf_stream, 'F')
    # pdf_stream.seek(0)

    s3.put_object(Bucket=AWS_S3_BUCKET_NAME, Key=f"dcz/teacher/{teacher_uuid}/")
    s3.upload_fileobj(file.file, AWS_S3_BUCKET_NAME, f"dcz/teacher/{teacher_uuid}/{file.filename}")
    # s3.upload_fileobj(pdf_stream, AWS_S3_BUCKET_NAME, f"dcz/teacher/{teacher_uuid}/{file.headers['filename']}.pdf")
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

def check_all_homeworks_admin(homeworks: List[Homework]):
  homeworks_all = []
  for homework in homeworks:
    end_time = datetime.fromisoformat(homework.end_date.replace("Z", '+00:00'))
    now_time = datetime.now(timezone.utc)
    left_time = end_time - now_time
    days_left = left_time.days
    homeworks_all.append({
      'homework_id': homework.homework_id,
      'title': homework.title,
      'timeleft': days_left, # 추가로 제출한 학생 테이블도 만들어서 컬럼 센 후에 오케이 해야함
    })
  return homeworks_all

# def check_detail_homework_admin(homework: Homework, db: Session):
#   db.query(Homework).filter(Homework.homework_id == homework.homework_id).all()
#   homework_detail = {
#     'title': homework.title,
#     'start_date': homework.start_date,
#     'end_date': homework.end_date,
#     'content': homework.
#   }

def check_all_homeworks_user(homeworks: List[Homework]):
  homeworks_all_for_user = []
  for homework in homeworks:
    end_time = datetime.fromisoformat(homework.end_date.replace("Z", '+00:00'))
    now_time = datetime.now(timezone.utc)
    left_time = end_time - now_time
    days_left = left_time.days
    homeworks_all_for_user.append({
      'homework_id': homework.homework_id,
      'title': homework.title,
      'timeleft': days_left,
      'teacher_name': homework.author.teacher_name if homework.author else None,
    })
  return homeworks_all_for_user