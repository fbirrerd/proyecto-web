from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.respond import objRespuesta
from app.database import SessionLocal
from app.schemas.moduloMenu import ModuloMenuCreate, ModuloMenuUpdate
from app.services.moduloMenu import create_modulo_menu, get_modulo_menu
from app.services.rol import get_lista


router = APIRouter(tags=["ModuloMenu"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def set_rol(rol: ModuloMenuCreate, db: Session = Depends(get_db)):
    datos = create_modulo_menu(db,rol)
    return  objRespuesta(
        respuesta=True,
        data=datos
    )    

@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_roles(db: Session = Depends(get_db)):
    datos = get_modulo_menu(db=db)
    return  objRespuesta(
        respuesta=True,
        data=datos
    )    


@router.get("/{rol_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_rol(rol_id: int, db: Session = Depends(get_db)):
    db_role = get_modulo_menu(db=db, rol_id=rol_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.put("/{rol_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def update_rol(rol_id: int, role: ModuloMenuUpdate, db: Session = Depends(get_db)):
    db_role = update_rol(db=db, rol_id=rol_id, role=role)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.get("/list/all", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_lista_roles(db: Session = Depends(get_db)):
    lista = get_lista(db)
    return objRespuesta(
        respuesta=True,
        data=lista
    )