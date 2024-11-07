from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from notification_comments import schemas, models
from notification_comments.database import get_db
from auth.auth import get_current_user

router = APIRouter()


@router.post("/notifications/{notification_id}/comments", response_model=schemas.Comments)
def create_comments(
  notification_id : int,
  comment: schemas.CreateComments,
  db: Session = Depends(get_db),
  current_user: models.User = Depends(get_current_user)  
):
  notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
  if notification is None:
    raise HTTPException(status_code=404, detail="존재하지 않는 공지사항 입니다.")
  
  db_comments = models.NotificationComments(
    content = comment.content,
    author_id = current_user.id,
    notification_id = notification_id
  )
  db.add(db_comments)
  db.commit()
  db.refresh(db_comments)
  
  return db_comments

@router.get("/notifications/{notification_id}/comments", response_model=list[schemas.Comments])
def get_comments(
  notification_id : int,
  db: Session = Depends(get_db),
):
  comments = db.query(models.NotificationComments).filter(models.NotificationComments.notification_id == notification_id).all()
  return comments