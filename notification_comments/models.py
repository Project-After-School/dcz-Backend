from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLAEnum, Date, VARCHAR, and_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, foreign
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
    
    comments = relationship(
        "NotificationComments",
        back_populates="user",
        primaryjoin="and_(foreign(NotificationComments.author_id) == User.id, "
                   "NotificationComments.author_type == 'user')"
    )

class Teacher(Base):
    __tablename__ = "teacher_info"
    
    id = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4, primary_key=True)
    teacher_id = Column(VARCHAR(100), nullable=False)
    teacher_name = Column(VARCHAR(5), nullable=False)
    email = Column(VARCHAR(100), nullable=False, unique=True)
    major = Column(VARCHAR(100), nullable=True)
    hashed_pw = Column(VARCHAR(100), nullable=False)
    role = Column(SQLAEnum(Role), default=Role.ADMIN)
    teacher_class = Column(VARCHAR(200), nullable=False)
    
    notifications = relationship("Notification", back_populates="author")
    comments = relationship(
        "NotificationComments",
        back_populates="teacher",
        primaryjoin="and_(foreign(NotificationComments.author_id) == Teacher.id, "
                   "NotificationComments.author_type == 'teacher')",
        overlaps="comments"
    )

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
    __tablename__ = 'notification_comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    author_id = Column(UUID, nullable=False)
    author_type = Column(String, nullable=False)  
    notification_id = Column(Integer, ForeignKey('notification.id'), nullable=False)
    date = Column(DateTime, default=datetime.now())

    user = relationship("User", 
                        primaryjoin="and_(NotificationComments.author_type == 'user', foreign(NotificationComments.author_id) == User.id)", 
                        back_populates="comments", 
                        uselist=False,
                        overlaps="comments")
    teacher = relationship("Teacher", 
                           primaryjoin="and_(NotificationComments.author_type == 'teacher', foreign(NotificationComments.author_id) == Teacher.id)", 
                           back_populates="comments", 
                           uselist=False,
                           overlaps="comments,user")

    notification = relationship("Notification", back_populates="comments")

