from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.respond import objRespuesta
from app.database import SessionLocal
from app.schemas.empresaModulo import (
    EmpresaModuloCreate,
    EmpresaModuloRelacion,
    EmpresaModuloUpdate,
)
from app.services.empresaModulo import (
    create_empresa_modulo,
    create_relacion_empresa_modulo,
    get_empresa_modulo,
    get_empresas_modulo,
    get_empresas_modulo_X_empresa,
    update_empresa_modulo,
)

router = APIRouter(tags=["EmpresaModulo"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def crear_empresa_modulo(obj: EmpresaModuloCreate, db: Session = Depends(get_db)):
    try:
        datos = create_empresa_modulo(db, obj)
        return objRespuesta(respuesta=True, data=datos)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al crear empresa-módulo: {str(e)}")

@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def listar_empresas_modulo(db: Session = Depends(get_db)):
    try:
        datos = get_empresa_modulo(db)
        return objRespuesta(respuesta=True, data=datos)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al obtener lista: {str(e)}")

@router.get("/{empresa_modulo_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_empresa_modulo(empresa_modulo_id: int, db: Session = Depends(get_db)):
    try:
        resultado = get_empresa_modulo(db, empresa_modulo_id)
        if resultado is None:
            return objRespuesta(respuesta=False, data="Empresa módulo no encontrada")
        return objRespuesta(respuesta=True, data=resultado)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al obtener registro: {str(e)}")

@router.put("/{empresa_modulo_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def actualizar_empresa_modulo(empresa_modulo_id: int, obj: EmpresaModuloUpdate, db: Session = Depends(get_db)):
    try:
        actualizado = update_empresa_modulo(db, empresa_modulo_id, obj)
        if actualizado is None:
            return objRespuesta(respuesta=False, data="Empresa módulo no encontrada")
        return objRespuesta(respuesta=True, data=actualizado)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al actualizar: {str(e)}")

@router.get("/list/all", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def listar_todos_los_registros(db: Session = Depends(get_db)):
    try:
        lista = get_empresas_modulo(db)
        return objRespuesta(respuesta=True, data=lista)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al listar registros: {str(e)}")

@router.get("/empresa/{empresa_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def listar_por_empresa(empresa_id: int, db: Session = Depends(get_db)):
    try:
        lista = get_empresas_modulo_X_empresa(db, empresa_id)
        return objRespuesta(respuesta=True, data=lista)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al obtener registros por empresa: {str(e)}")

@router.post("/guardar-relacion", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def guardar_relacion(obj: EmpresaModuloRelacion, db: Session = Depends(get_db)):
    try:
        datos = create_relacion_empresa_modulo(db, obj)
        return objRespuesta(respuesta=True, data=datos)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al guardar relación: {str(e)}")
