from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.respond import objRespuesta
from app.database import SessionLocal
from app.schemas.empresa import EmpresaCreate, EmpresaOut


router = APIRouter(tags=["EmpresaUsuario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

