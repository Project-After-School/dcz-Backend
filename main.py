from fastapi import FastAPI
from user_login.routes import user as user_router
from notification import router as notification_router
from notification_comments import router as comments_router
from fastapi.middleware.cors import CORSMiddleware
from admin.router import admin_router
from user_mypage import router as user_mypage_router
from admin.database.admin import init_teacher_db
from homework.database.homework import init_homework_db
from auth import auth as auth_router
from homework.routes import homework as homework_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router, tags=["유저"]) # 유저
app.include_router(notification_router.router, tags=["공지"]) # 공지
app.include_router(admin_router.router, tags=['어드민 로그인 회원가입']) # 어드민 로그인 회원가입
app.include_router(comments_router.router, tags=['공지사항 댓글']) 
app.include_router(user_mypage_router.router, tags=['유저 마이페이지'])
app.include_router(homework_router.router, tags=['과제'])

if __name__ == "__main__":
    init_teacher_db()
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)