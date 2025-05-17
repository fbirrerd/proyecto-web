from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.empresaUsuarioRol import obtener_roles_por_empresa_usuario
from app.services.empresaUsuario import setEmpresaUsuario
from app.schemas.empresaUsuarioRol import EmpresaUsuarioRolCreate
from app.schemas.respond import objRespuesta
from app.database import SessionLocal

router = APIRouter(tags=["EmpresaUsuarioRol"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/permisos", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_roles_empresa_usuario(db: Session = Depends(get_db)):
    try:
        data = obtener_roles_por_empresa_usuario(db)
        return objRespuesta(respuesta=True, data=data)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al obtener permisos: {str(e)}")

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def guardar_relacion(oCreate: EmpresaUsuarioRolCreate, db: Session = Depends(get_db)):
    try:
        resultado = setEmpresaUsuario(db, oCreate.id_empresa, oCreate.id_usuario)
        return objRespuesta(respuesta=True, data=resultado)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al guardar relación: {str(e)}")
