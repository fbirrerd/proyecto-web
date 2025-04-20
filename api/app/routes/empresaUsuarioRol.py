from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.empresa import EmpresaCreate, EmpresaOut


router = APIRouter(tags=["EmpresaUsuarioRol"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
