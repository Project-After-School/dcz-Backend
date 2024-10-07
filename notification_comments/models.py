from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Enum
from notification.database import Base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from sqlalchemy.orm import relationship
import enum

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
    role = Column(Enum(Role), nullable=False)
    notifications = relationship("Notification", back_populates="author")  
    content = relationship("NotificationComments", back_populates="author")

class Notification(Base):
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    date = Column(DateTime, nullable=False , default=datetime.now)
    author_id = Column(UUID(as_uuid=True), ForeignKey("user_info.id"))  
    author = relationship("User", back_populates="notifications")  
    content = relationship("NotificationComments", back_populates="notifications")



class NotificationComments(Base):
    __tablename__ = "notification_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    date = Column(DateTime, nullable=False , default=datetime.now)
    
    author_id = Column(UUID(as_uuid=True), ForeignKey("user_info.id"))  
    notification_id = Column(Integer, ForeignKey("notification.id"))
    
    author = relationship("User", back_populates="notification_comments")
    notification = relationship("Notification", back_populates="notification_comments")

    

    
