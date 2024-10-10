from fastapi import FastAPI
from user_login.routes import user as user_router
from notification import router as notification_router
from notification_comments import router as comments_router
from fastapi.middleware.cors import CORSMiddleware
# from admin_singin import admin_router

app =FastAPI(
  
)
origins = [
  "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router, tags=["유저"]) # 유저
app.include_router(notification_router.router, tags=["공지"]) # 공지
# app.include_router(admin_router.router, tags=['어드민 로그인'])
app.include_router(comments_router.router, tags=['공지사항 댓글'])

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)