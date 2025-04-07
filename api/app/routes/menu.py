from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.menu import MenuTree
from app.database import SessionLocal


router = APIRouter(tags=["Menu"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

