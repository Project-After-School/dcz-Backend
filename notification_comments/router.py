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
    comment: CreateComments,  # content만 받음
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 공지사항 확인
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if notification is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 공지사항입니다.")

    # 댓글 생성
    db_comments = models.NotificationComments(
        content=comment.content,
        author_id=current_user.id,  # 현재 사용자의 id를 author_id로 설정
        author_type="user",  # 'user'로 설정
        notification_id=notification_id,
        date=datetime.utcnow()  # 작성 날짜
    )
    
    # DB에 저장
    db.add(db_comments)
    db.commit()
    db.refresh(db_comments)

    # 댓글 반환 (author 정보 포함)
    db_comments.author = current_user  # 현재 로그인된 사용자를 author로 설정
    return db_comments


@router.post("/admin/notifications/{notification_id}/comments", response_model=NotificationComments)
def create_teacher_comments(
    notification_id: int,
    comment: CreateComments,  # content만 받음
    db: Session = Depends(get_db),
    current_teacher: Teacher = Depends(get_current_teacher)
):
    # 공지사항 확인
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if notification is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 공지사항입니다.")

    # 댓글 생성
    db_comments = models.NotificationComments(
        content=comment.content,
        author_id=current_teacher.id,  # 현재 선생님의 id를 author_id로 설정
        author_type="teacher",  # 'teacher'로 설정
        notification_id=notification_id,
        date=datetime.utcnow()  # 작성 날짜
    )
    
    # DB에 저장
    db.add(db_comments)
    db.commit()
    db.refresh(db_comments)

    # 댓글 반환 (author 정보 포함)
    db_comments.author = current_teacher  # 현재 로그인된 선생님을 author로 설정
    return db_comments
  
@router.get("/notifications/{notification_id}/comments", response_model=list[schemas.Notificationget])
def get_comments(
  notification_id: int,
  db: Session = Depends(get_db),
):
    comments = db.query(models.NotificationComments).filter(models.NotificationComments.notification_id == notification_id).all()

    # 각 댓글에 대해 작성자 이름을 추가
    for comment in comments:
        if comment.author_type == "user":
            user = db.query(models.User).filter(models.User.id == comment.author_id).first()
            comment.author_name = user.name if user else "Unknown User"
        elif comment.author_type == "teacher":
            teacher = db.query(models.Teacher).filter(models.Teacher.id == comment.author_id).first()
            comment.author_name = teacher.teacher_name if teacher else "Unknown Teacher"
    
    return comments