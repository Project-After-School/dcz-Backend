from sqlalchemy import Column, Integer, VARCHAR, Enum, UUID, String, Date
from sqlalchemy.orm import relationship
from ..database.admin import Base
# from user_login.models.user import Role
import enum
import uuid

class Role(enum.Enum):
    STU = "STU"
    ADMIN = "ADMIN"

class Teacher(Base):
  __tablename__ = "teacher_info"

  teacher_id = Column(VARCHAR(100), primary_key=True, nullable=False)
  teacher_name = Column(VARCHAR(5), nullable=False)
  email = Column(VARCHAR(100), nullable=False, unique=True)
  major = Column(VARCHAR(100), nullable=True)
  hashed_pw = Column(VARCHAR(100), nullable=False)
  role = Column(Enum(Role), default=Role.ADMIN)