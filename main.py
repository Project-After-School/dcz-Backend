from fastapi import FastAPI
from user_login.routes import user
from notification import router
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(user.router)
app.include_router(router.router)