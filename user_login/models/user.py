from sqlalchemy import Column, String, Integer, Date, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
import enum
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
    role = Column(Enum(Role), nullable=False)

