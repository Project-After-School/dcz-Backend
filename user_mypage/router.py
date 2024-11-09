from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from user_mypage import schemas, models
from user_mypage.database import get_db
from auth.auth import get_current_user

router = APIRouter(
  
)

@router.get("/get_user_mypage", response_model=schemas.Mypage)
def get_user_mypage(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    
    if not user:
      raise HTTPException(status_code=404, detail="존재하지 않는 유저 입니다")
    
    return {
      "name" : user.name,
      "grade" : user.grade,
      "class_num" : user.class_num,
      "num" : user.num,
      "profile"  : user.profile
  
    }
   