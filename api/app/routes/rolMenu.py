from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.rolMenu import ObjetoRelaciones
from app.schemas.respond import objRespuesta
from app.database import SessionLocal
from app.services.RolMenu import get_RolMenu, set_relaciones



router = APIRouter(tags=["RolMenu"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_RolMenu(db: Session = Depends(get_db)):
    data = get_RolMenu(db=db)
    return datos
    try:
        data = get_all(db=db)
        return objRespuesta(
            respuesta = True, 
            data=usuarios
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al obtener registros: {str(e)}"
        )


@router.post("/guardar-relaciones", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def set_relations(relaciones: ObjetoRelaciones, db: Session = Depends(get_db)):
    try:
        data = set_relaciones(db, relaciones)
        return datos
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al crear registro: {str(e)}"
        )
