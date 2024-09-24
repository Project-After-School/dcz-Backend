from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://yabbi:12341234@43.203.215.239:5432/dcz"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush= False, autocommit = False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()  # 세션 생성
    try:
        yield db
    except Exception as e:
        print(f"Database error: {e}")  # 로그 추가
        raise  # 예외를 다시 발생시킴
    finally:
        db.close()
