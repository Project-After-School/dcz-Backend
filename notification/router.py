from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from notification import schemas, models
from notification.database import get_db
from auth.auth import get_current_user, get_current_teacher
from sqlalchemy import func

router = APIRouter()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db
from admin.models import admin as Admin

router = APIRouter()


@router.post("/admin/post_notification", response_model=schemas.Notification)
def create_notification(
    notification: schemas.NotificationCreate,
    db: Session = Depends(get_db),
    current_teacher: models.Teacher = Depends(get_current_teacher)
):
    db_notification = models.Notification(
        title=notification.title,
        content=notification.content,
        grade=", ".join(notification.grade),  
        class_num=", ".join(notification.class_num),  
        author_id=current_teacher.id  
    )

    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    return {
        **db_notification.__dict__,
        "author_name": current_teacher.teacher_name,
        "grade": db_notification.grade.split(', '),  
        "class_num": db_notification.class_num.split(', ')  
    }



@router.put("/admin/update_notification", response_model=schemas.Notification)
def update_notification(
    notification_id: int,
    notification_update: schemas.NotificationUpdate,
    db: Session = Depends(get_db),
    current_teacher: models.Teacher = Depends(get_current_teacher)  
):
    
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 공지사항 입니다.")
    
    if db_notification.author_id != current_teacher.id:
        raise HTTPException(status_code=403, detail="수정할 권한이 없습니다.")
    
    
    db_notification.title = notification_update.title
    db_notification.content = notification_update.content
    
    db_notification.grade = ", ".join(notification_update.grade)
    db_notification.class_num = ", ".join(notification_update.class_num) 

   
    db.commit()
    db.refresh(db_notification)

    return {
        **db_notification.__dict__,
        "author_name": current_teacher.teacher_name ,
        "grade":  db_notification.grade.split(', '),
        "class_num": db_notification.class_num.split(' ,')
        
    }

    
    

@router.get("/get_notification_all_admin", response_model=list[schemas.NotificationSimple])
def get_notification_all_admin(
    db: Session = Depends(get_db),
    current_teacher: models.Teacher = Depends(get_current_teacher)
):
    notifications = db.query(models.Notification).filter(models.Notification.author_id == current_teacher.id).all()

    notifications_with_author = []
    for notification in notifications:
        author = db.query(models.Teacher).filter(models.Teacher.id == notification.author_id).first()
        notifications_with_author.append({
            "title": notification.title,
            "id": notification.id,
            "date": notification.date,
            "grade": notification.grade,
            "class_num": notification.class_num,
            "major": author.major if author else None  
        })

    return notifications_with_author


@router.get("/get_notification_all_user", response_model=list[schemas.NotificationSimple])
def get_notification_all_user(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    notifications = db.query(models.Notification).filter(
        models.Notification.grade.like(f"%{current_user.grade}%"),
        models.Notification.class_num.like(f"%{current_user.class_num}%")
    ).all()

    notifications_with_author = []
    for notification in notifications:
        author = db.query(models.Teacher).filter(models.Teacher.id == notification.author_id).first()
        notifications_with_author.append({
            "title": notification.title,
            "id": notification.id,
            "date": notification.date,
            "grade": notification.grade,
            "class_num": notification.class_num,
            "major": author.major if author else None  
        })

    return notifications_with_author


@router.get("/get_notification_detail", response_model=schemas.Notification)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 공지사항 입니다.")

    author_name = None
    author_id = db_notification.author_id
    
    user_author = db.query(models.User).filter(models.User.id == author_id).first()
    if user_author:
        author_name = user_author.name
    else:
        teacher_author = db.query(models.Teacher).filter(models.Teacher.id == author_id).first()
        if teacher_author:
            author_name = teacher_author.teacher_name
    
    if not author_name:
        raise HTTPException(status_code=404, detail="작성자를 찾을 수 없습니다.")

    return {
        **db_notification.__dict__,
        "author_name": author_name,
        "date": db_notification.date,
        "grade": db_notification.grade.split(', '),
        "class_num": db_notification.class_num.split(', ')
    }

        
    
    
    
    
    

@router.delete("/admin/delete_notification", response_model=schemas.Notification)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_teacher: models.Teacher = Depends(get_current_teacher)
):
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 공지사항 입니다.")
    
    if db_notification.author_id != current_teacher.id:
        raise HTTPException(status_code=403, detail="삭제할 권한이 없습니다.")
    
    db.query(models.NotificationComments).filter(models.NotificationComments.notification_id == notification_id).delete()
    
    db.delete(db_notification)
    db.commit()
    
    return {
        **db_notification.__dict__,
        "author_name": current_teacher.teacher_name,
        "grade": db_notification.grade.split(', '),
        "class_num": db_notification.class_num.split(', ')
    }





@router.delete("/admin/delete_notification_all", response_model=list[schemas.Notification])
def delete_notification_all(
    db: Session = Depends(get_db),
    current_teacher: models.Teacher = Depends(get_current_teacher)  
):
    
    db_notifications = db.query(models.Notification).all()
    
    if not db_notifications:
        raise HTTPException(status_code=404, detail="삭제할 공지사항이 없습니다.")
    

    deleted_notifications = [] 
    for notification in db_notifications:
        deleted_notifications.append({
            "id": notification.id,
            "title": notification.title,
            "content": notification.content,
            "author_id": notification.author_id,
            "date": notification.date, 
        })
        db.delete(notification)
    
    db.commit()

    return deleted_notifications  
