from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLAEnum, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

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

    notifications = relationship("Notification", back_populates="author")


class Notification(Base):
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    date = Column(DateTime, nullable=False, default=datetime.now)
    author_id = Column(UUID(as_uuid=True), ForeignKey("user_info.id"))

    # 지연 임포트 사용
    author = relationship("User", back_populates="notifications")
