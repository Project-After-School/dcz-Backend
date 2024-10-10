from sqlalchemy.orm import Session
from admin_signin.admin_schema import NewAdminForm
from admin_signin.models import Teacher
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_admin(email: str, db: Session):
  return db.query(Teacher).filter(Teacher.email == email).first()

def create_admin(new_admin: NewAdminForm, db: Session):
  admin = Teacher(
    teacher_id = new_admin.teacher_id,
    teacher_name = new_admin.name,
    email = new_admin.email,
    hashed_pw = pwd_context.hash(new_admin.password),
    major = new_admin.major
  )
  db.add(admin)
  db.commit()