from sqlalchemy import Column, Integer, String
from database import Base
from datetime import datetime



class notification(Base):
  __tablename__ = "notification"
  
  id = Column(Integer)
  title = Column