from sqlalchemy import Column, Integer, VARCHAR, String, DateTime, TEXT, Boolean
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from enum import Enum
from homework.database.homework import Base
from typing import List


class Homework(Base):
  __tablename__ = "homework"

  homework_id = Column(Integer, primary_key=True, index=True, autoincrement=True) # db 과제 제출 식별자
  title = Column(VARCHAR(100), nullable=False, index=True) # 제목
  content = Column(TEXT, nullable=False) # 내용
  submit_detail = Column(TEXT, nullable=False) # 제출 양식
  start_date = Column(DateTime, nullable=False)
  end_date = Column(DateTime, nullable=False)
  teacher_file_url = Column(String, nullable=True)
  selected_grade = Column(VARCHAR(200), nullable=False) # 선택한 학년반 값 "1-1,1-2,2-1"와 같이 전달
  author_id = Column(VARCHAR(100), ForeignKey("teacher.teacher_id"), index=True)
  major = Column(VARCHAR(20), ForeignKey("teacher.major"), index=True)

  teacher = relationship("Teacher", back_populates="homework")

class HomeworkFile(Base):
  __tablename__ = "homeworkfile"

  hf_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  homework_id = Column(Integer, ForeignKey("homework.homework_id"))
  student_id = Column(String(40), ForeignKey("user_info.account_id"))
  student_name = Column(String(10), ForeignKey("user_info.name"))
  file_url = Column(String, nullable=True)
  grade = Column(Integer, ForeignKey("user_info.grade"))
  class_num = Column(Integer, ForeignKey("user_info.class_num"))
  check_submit = Column(Boolean, nullable=False)

  homework = relationship("Homework", back_populates="homeworkfile")
  user = relationship("User", back_populates="homeworkfile")