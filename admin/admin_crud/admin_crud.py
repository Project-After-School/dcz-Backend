from sqlalchemy.orm import Session
from admin.models.admin import Teacher
from admin.schemas.admin import NewAdminForm
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_admin(teacher_id: str, db: Session):
  return db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()

def create_admin(new_admin: NewAdminForm, db: Session):
  admin = Teacher(
    dcz_id = uuid.uuid4(),
    teacher_id = new_admin.teacher_id,
    teacher_name = new_admin.name,
    email = new_admin.email,
    hashed_pw = pwd_context.hash(new_admin.password),
    major = new_admin.major,
    teacher_class = new_admin.teacher_class
  )
  db.add(admin)
  db.commit()

def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)