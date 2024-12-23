from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  except Exception as e:
    db.close()
    raise e
  finally:
    db.close()

def init_homework_db():
  Base.metadata.create_all(engine)