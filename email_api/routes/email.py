from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db

from email import EmailCreate, EmailOut
from schemas.respond import objRespuesta

router = APIRouter(
    prefix="/emails",
    tags=["Emails"]
)

@router.post("/", response_model=objRespuesta)
def create_email(email: EmailCreate, db: Session = Depends(get_db)):
    return create_email(db, email)

@router.get("/pendientes", response_model=objRespuesta)
def get_pending_emails(db: Session = Depends(get_db)):
    return get_pending_emails(db)
