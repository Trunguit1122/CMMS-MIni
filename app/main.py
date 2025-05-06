# app/main.py

from fastapi import FastAPI
from app.api import auth  
from app.api import profile  
app = FastAPI()

# Gắn router
app.include_router(auth.router)
app.include_router(profile.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}
