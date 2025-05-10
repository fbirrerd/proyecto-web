from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.respond import objRespuesta
from app.database import SessionLocal
from app.schemas.modulo import ModuloCreate, ModuloUpdate
from app.services.modulo import create_modulo, get_modulo, get_modulos, update_modulo


router = APIRouter(tags=["Modulo"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def set_rol(rol: ModuloCreate, db: Session = Depends(get_db)):
    datos = create_modulo(db,rol)
    return  objRespuesta(
        respuesta=True,
        data=datos
    )    

@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_roles(db: Session = Depends(get_db)):
    datos = get_modulos(db)
    return  objRespuesta(
        respuesta=True,
        data=datos
    )    


@router.get("/{modulo_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_rol(modulo_id: int, db: Session = Depends(get_db)):
    db_role = get_modulo(db, modulo_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.put("/{modulo_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def update_rol(modulo_id: int, obj: ModuloUpdate, db: Session = Depends(get_db)):
    db_role = update_modulo(db, modulo_id, obj)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

# @router.get("/list/all", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
# def obtener_lista_roles(db: Session = Depends(get_db)):
#     lista = get_lista(db)
#     return objRespuesta(
#         respuesta=True,
#         data=lista
#     )