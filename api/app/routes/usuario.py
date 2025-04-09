from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import true
from sqlalchemy.orm import Session
from app.schemas.respond import objRespuesta
from app.database import SessionLocal

router = APIRouter(tags=["Usuario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

