from sqlalchemy import Column, Integer, VARCHAR, Enum
from admin_signin.database import Base
from user_login.models.user import Role

class Teacher(Base):
  __tablename__ = "teacher"

  teacher_id = Column(Integer, primary_key=True, autoincrement=True)
  email = Column(VARCHAR(100), nullable=False, unique=True)
  teacher_name = Column(VARCHAR(5), nullable=False)
  major = Column(VARCHAR(100), nullable=False, default='과목 없음')
  hashed_pw = Column(VARCHAR(100), nullable=False)
  role = Column(Enum(Role), default=Role.ADMIN)