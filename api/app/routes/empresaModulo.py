from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.respond import objRespuesta
from app.database import SessionLocal
from app.schemas.empresaModulo import EmpresaModuloCreate, EmpresaModuloRelacion, EmpresaModuloUpdate
from app.services.empresaModulo import create_empresa_modulo, create_relacion_empresa_modulo, get_empresa_modulo, get_empresas_modulo, get_empresas_modulo_X_empresa, update_empresa_modulo


router = APIRouter(tags=["EmpresaModulo"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def set_rol(obj: EmpresaModuloCreate, db: Session = Depends(get_db)):
    datos = create_empresa_modulo(db,obj)
    return  objRespuesta(
        respuesta=True,
        data=datos
    )    

@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_registers(db: Session = Depends(get_db)):
    datos = get_empresa_modulo(db=db)
    return  objRespuesta(
        respuesta=True,
        data=datos
    )    

@router.get("/{empresa_modulo_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_register(empresa_modulo_id: int, db: Session = Depends(get_db)):
    db_role = get_empresa_modulo(db, empresa_modulo_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.put("/{empresa_modulo_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def update_rol(empresa_modulo_id: int, obj: EmpresaModuloUpdate, db: Session = Depends(get_db)):
    db_role = update_empresa_modulo(db,empresa_modulo_id , obj)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.get("/list/all", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_lista_roles(db: Session = Depends(get_db)):
    lista = get_empresas_modulo(db)
    return objRespuesta(
        respuesta=True,
        data=lista
    )
    
@router.get("/empresa/{empresa_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_lista_roles(empresa_id: int, db: Session = Depends(get_db)):
    lista = get_empresas_modulo_X_empresa(db, empresa_id)
    return objRespuesta(
        respuesta=True,
        data=lista
    )    

@router.post("/guardar-relacion", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def set_rol(obj: EmpresaModuloRelacion, db: Session = Depends(get_db)):
    datos = create_relacion_empresa_modulo(db,obj)
    return  objRespuesta(
        respuesta=True,
        data=datos
    ) 