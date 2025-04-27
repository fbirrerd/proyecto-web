from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.rolMenu import ObjetoRelaciones
from app.services.RolMenu import get_RolMenu, set_relaciones
from app.schemas.respond import objRespuesta
from app.database import SessionLocal


router = APIRouter(tags=["RolMenu"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_RolMenu(db: Session = Depends(get_db)):
    datos = get_RolMenu(db=db)
    return datos


@router.post("/guardar-relaciones", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def set_relations(relaciones: ObjetoRelaciones, db: Session = Depends(get_db)):
    datos = set_relaciones(db, relaciones)
    return datos
