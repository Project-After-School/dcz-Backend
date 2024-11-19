from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from typing import Optional
import os

load_dotenv()
DATABASE_URL = os.getenv("URL")
DB_URL = os.getenv("DATABASE_URL")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Settings(BaseSettings):
  SECRET_KEY: Optional[str] = None
  DATABASE_URL: Optional[str] = None
  COOKIE_NAME: str = "teacher_cookie"
  COOKIE_DOMAIN: str = DATABASE_URL
  COOKIE_PATH: str = "/"
  COOKIE_SECURE: bool = False # HTTPS로 사용한다면 True
  COOKIE_HTTPONLY: bool = True
  COOKIE_SAMESITE: str = "Lax"
  
  class Config:
    env_file = ".env"

def get_db():
  db = SessionLocal()
  try:
    yield db
  except Exception as e:
    db.close()
    raise e
  finally:
    db.close()

def init_teacher_db():
  Base.metadata.create_all(engine)