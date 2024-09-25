from fastapi import FastAPI
from user_login.routes import user
app =FastAPI(
  
)

app.include_router(user.router)