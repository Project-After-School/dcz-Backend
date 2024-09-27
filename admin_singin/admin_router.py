from fastapi import APIRouter
import admin_schema

router = APIRouter(
  prefix="/admin"
)

@router.post('/signup')
async def signup(new_user: admin_schema.NewAdminForm):
  