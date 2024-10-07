from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from admin_signin.database import get_db
import admin_signin.admin_schema as admin_schema
import admin_signin.admin_crud as admin_crud

router = APIRouter(
  prefix="/admin"
)

@router.post('/signup')
async def signup(new_teacher: admin_schema.NewAdminForm, db: Session = Depends(get_db)):
  teacher = admin_crud.get_admin(new_teacher.email, db)

  if teacher:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')

  admin_crud.create_admin(new_teacher, db)

  return HTTPException(status_code=status.HTTP_200_OK, detail="Singup Succeed")