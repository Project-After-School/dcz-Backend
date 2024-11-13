from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from notification_comments import schemas, models
from notification_comments.database import get_db
from auth.auth import get_current_user, get_current_teacher
from notification_comments.schemas import CreateComments, NotificationComments
from notification_comments.models import User, Teacher
from datetime import datetime


router = APIRouter()

@router.post("/user/notifications/{notification_id}/comments", response_model=NotificationComments)
def create_user_comments(
    notification_id: int,
    comment: CreateComments,  
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if notification is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 공지사항입니다.")

    db_comments = models.NotificationComments(
        content=comment.content,
        author_id=current_user.id,  
        author_type="user", 
        notification_id=notification_id,
        date=datetime.utcnow()  
    )
    
    db.add(db_comments)
    db.commit()
    db.refresh(db_comments)

    db_comments.author = current_user 
    return db_comments


@router.post("/admin/notifications/{notification_id}/comments", response_model=NotificationComments)
def create_teacher_comments(
    notification_id: int,
    comment: CreateComments,  
    db: Session = Depends(get_db),
    current_teacher: Teacher = Depends(get_current_teacher)
):
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if notification is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 공지사항입니다.")

    db_comments = models.NotificationComments(
        content=comment.content,
        author_id=current_teacher.id, 
        author_type="teacher",  
        notification_id=notification_id,
        date=datetime.utcnow() 
    )
    
    db.add(db_comments)
    db.commit()
    db.refresh(db_comments)

    db_comments.author = current_teacher  
    return db_comments
  
@router.get("/notifications/{notification_id}/comments", response_model=list[schemas.Notificationget])
def get_comments(
  notification_id: int,
  db: Session = Depends(get_db),
):
    comments = db.query(models.NotificationComments).filter(models.NotificationComments.notification_id == notification_id).all()

    for comment in comments:
        if comment.author_type == "user":
            user = db.query(models.User).filter(models.User.id == comment.author_id).first()
            comment.author_name = user.name if user else "Unknown User"
        elif comment.author_type == "teacher":
            teacher = db.query(models.Teacher).filter(models.Teacher.id == comment.author_id).first()
            comment.author_name = teacher.teacher_name if teacher else "Unknown Teacher"
    
    return comments