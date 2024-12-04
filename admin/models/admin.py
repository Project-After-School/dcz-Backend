from sqlalchemy import Column, Integer, VARCHAR, Enum as SQLEnum, UUID, String, Date, TEXT
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

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # 기본 키
    teacher_id = Column(String(100), nullable=False, unique=True)  # 유니크 제약 조건
    teacher_name = Column(String(5), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    major = Column(String(100), nullable=True)
    hashed_pw = Column(String(100), nullable=False)
    role = Column(SQLEnum(Role), default=Role.ADMIN)
    teacher_class = Column(String(200))  # 선생님의 담당 학년반

    # Homework와의 관계근ㄷ모
    # homework = relationship("Homework", back_populates="author")