from fastapi import FastAPI
import uvicorn

app =FastAPI(
  
)
from src.router import router

app.include_router(router)