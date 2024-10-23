from sqlalchemy import Column, Integer, VARCHAR, Enum, UUID, String, Date
from sqlalchemy.orm import relationship
from ..database.admin import Base
# from user_login.models.user import Role
import enum
import uuid

class Role(enum.Enum):
  STU = "STU"
  ADMIN = "ADMIN"

class SchoolClass(enum.Enum):
  ONEONE = "ONEONE" # 1-1
  ONETWO = "ONETWO" # 1-2
  ONETHREE = "ONETHREE" # 1-3
  ONEFOUR = "ONEFOUR" # 1-4
  TWOONE = "TWOONE" # 2-1
  TWOTWO = "TWOTWO" # 2-2
  TWOTHREE = "TWOTHREE" # 2-3
  TWOFOUR = "TWOFOUR" # 2-4
  THREEONE = "THREEONE" # 3-1
  THREETWO = "THREETWO" # 3-2
  THREETHREE = "THREETHREE" # 3-3
  THREEFOUR = "THREEFOUR" # 3-4
  

class Teacher(Base):
  __tablename__ = "teacher_info"

  teacher_id = Column(VARCHAR(100), primary_key=True, nullable=False)
  teacher_name = Column(VARCHAR(5), nullable=False)
  email = Column(VARCHAR(100), nullable=False, unique=True)
  major = Column(VARCHAR(100), nullable=True)
  hashed_pw = Column(VARCHAR(100), nullable=False)
  role = Column(Enum(Role), default=Role.ADMIN)
  teacher_class = Column(Enum(SchoolClass))