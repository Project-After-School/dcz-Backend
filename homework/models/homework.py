from sqlalchemy import Column, Integer, VARCHAR, String, DateTime, TEXT, Boolean, Enum as SQLAEnum, Date, Enum
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
# from enum import Enum
from homework.database.homework import Base
from sqlalchemy.dialects.postgresql import UUID
import enum
import uuid
from typing import List

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
    role = Column(SQLAEnum(Role), default=Role.ADMIN)
    teacher_class = Column(String(200))  # 선생님의 담당 학년반

    # Homework와의 관계
    homework = relationship("Homework", back_populates="author")


class User(Base):
    __tablename__ = "user_info"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # 기본 키
    xquare_id = Column(UUID(as_uuid=True), nullable=False)  # UUID 필드
    account_id = Column(String(40), nullable=False, unique=True)  # 유니크 제약 조건
    name = Column(String(10), nullable=False)
    grade = Column(Integer, nullable=False)
    class_num = Column(Integer, nullable=False)
    num = Column(Integer, nullable=False)
    birth_day = Column(Date, nullable=False)
    device_token = Column(String, nullable=True)
    profile = Column(String, nullable=True)
    role = Column(SQLAEnum(Role), nullable=False, default=Role.STU)

    # HomeworkFile과의 관계
    homeworkfile = relationship("HomeworkFile", back_populates="user_info")


class Homework(Base):
    __tablename__ = "homework"

    homework_id = Column(Integer, primary_key=True, autoincrement=True)  # 기본 키
    title = Column(String(100), nullable=False, index=True)  # 제목
    content = Column(TEXT, nullable=False)  # 내용
    submit_detail = Column(TEXT, nullable=False)  # 제출 양식
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    teacher_file_url = Column(String, nullable=True, default=None)
    selected_grade = Column(String(200), nullable=False)  # 선택한 학년반 값
    author_id = Column(UUID(as_uuid=True), ForeignKey("teacher_info.id"), index=True)  # 외래 키

    # Teacher와의 관계
    author = relationship("Teacher", back_populates="homework")

    # HomeworkFile과의 관계
    homeworkfile = relationship("HomeworkFile", back_populates="homework")


class HomeworkFile(Base):
    __tablename__ = "homeworkfile"

    hf_id = Column(Integer, primary_key=True, autoincrement=True)  # 기본 키
    homework_id = Column(Integer, ForeignKey("homework.homework_id"))  # Homework와의 외래 키
    student_id = Column(String(40), ForeignKey("user_info.account_id"))  # User와의 외래 키
    file_url = Column(String, nullable=True)
    check_submit = Column(Boolean, nullable=False)

    # Homework와의 관계
    homework = relationship("Homework", back_populates="homeworkfile")

    # User와의 관계
    user_info = relationship("User", back_populates="homeworkfile")