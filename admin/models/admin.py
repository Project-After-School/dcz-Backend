from sqlalchemy import Column, Integer, VARCHAR, Enum, UUID, String, Date, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from admin.database.admin import Base

# from user_login.models.user import Role
import enum
import uuid

class Role(enum.Enum):
  STU = "STU"
  ADMIN = "ADMIN"

class Teacher(Base):
  __tablename__ = "teacher_info"

  dcz_id = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4, primary_key=True)
  teacher_id = Column(VARCHAR(100), nullable=False)
  teacher_name = Column(VARCHAR(5), nullable=False)
  email = Column(VARCHAR(100), nullable=False, unique=True)
  major = Column(VARCHAR(100), nullable=True)
  hashed_pw = Column(VARCHAR(100), nullable=False)
  role = Column(Enum(Role), default=Role.ADMIN)
  teacher_class = Column(VARCHAR(200), nullable=False)