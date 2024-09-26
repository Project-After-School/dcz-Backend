from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from notification import schemas, models
from notification.database import get_db
from notification.auth import get_current_user

router = APIRouter()

@router.post("/admin/post_notification", response_model=schemas.Notification)
def create_notification(
    notification: schemas.NotificationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # 인증 확인
):
    db_notification = models.Notification(**notification.dict(), author_id=current_user.id)
    
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return {
        **db_notification.__dict__,
        "author_name": current_user.name  
    }

@router.put("/admin/update_notification", response_model=schemas.Notification)
def update_notification(
    notification_id: int,
    notification_update: schemas.NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # 인증 확인
):
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 공지사항 입니다.")
    
    # 수정할 내용 업데이트
    db_notification.title = notification_update.title
    db_notification.content = notification_update.content
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.get("/get_notification_all", response_model=list[schemas.Notification])
def get_notification_all(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # 인증 확인
):
    notifications = db.query(models.Notification).offset(skip).limit(limit).all()
    return notifications

@router.get("/get_notification", response_model=schemas.Notification)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # 인증 확인
):
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 공지사항 입니다.")
    
    return db_notification

@router.delete("/admin/delete_notification", response_model=schemas.Notification)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # 인증 확인
):
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 공지사항 입니다.")
    
    db.delete(db_notification)
    db.commit()
    return db_notification
