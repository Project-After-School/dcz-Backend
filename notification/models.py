from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLAEnum, Date, VARCHAR,Enum 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid
from sqlalchemy.dialects.postgresql import ARRAY

#
Base = declarative_base()

class Role(enum.Enum):
    STU = "STU"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "user_info"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    xquare_id = Column(UUID(as_uuid=True), nullable=False)
    account_id = Column(String(40), nullable=False, unique=True)
    name = Column(String(10), nullable=False)
    grade = Column(Integer, nullable=False)
    class_num = Column(Integer, nullable=False)
    num = Column(Integer, nullable=False)
    birth_day = Column(Date, nullable=False)
    device_token = Column(String, nullable=True)
    profile = Column(String, nullable=True)
    role = Column(SQLAEnum(Role), nullable=False)

  
    
class Teacher(Base):
  __tablename__ = "teacher_info"
  
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # 기본 키
  teacher_id = Column(String(100), nullable=False, unique=True)  # 유니크 제약 조건
  teacher_name = Column(String(5), nullable=False)
  email = Column(String(100), nullable=False, unique=True)
  major = Column(String(100), nullable=True)
  hashed_pw = Column(String(100), nullable=False)
  role = Column(SQLAEnum(Role), default=Role.ADMIN)
  teacher_class = Column(String(200))
  
  notifications = relationship("Notification", back_populates="author")
  notification_comments = relationship("NotificationComments", back_populates="author")


class Notification(Base):
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    date = Column(DateTime, nullable=False, default=datetime.now())
    author_id = Column(UUID(as_uuid=True), ForeignKey("teacher_info.id"))
    grade = Column(String, nullable=False)  
    class_num = Column(String, nullable=False)  

    author = relationship("Teacher", back_populates="notifications")
    comments = relationship("NotificationComments", back_populates="notification")


class NotificationComments(Base):
    __tablename__ = "notification_comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now())

    author_id = Column(UUID(as_uuid=True), ForeignKey("teacher_info.id"))
    notification_id = Column(Integer, ForeignKey("notification.id"))

    author = relationship("Teacher", back_populates="notification_comments")
    notification = relationship("Notification", back_populates="comments")