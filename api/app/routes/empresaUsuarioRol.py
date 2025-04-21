from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.app.schemas.empresaUsuarioRol import EmpresaUsuarioRolCreate
from api.app.schemas.respond import objRespuesta
from api.app.services.empresaUsuario import setEmpresaUsuario
from api.app.services.empresaUsuarioRol import obtener_empresa_usuario_roles
from app.database import SessionLocal
from app.schemas.empresa import EmpresaCreate, EmpresaOut


router = APIRouter(tags=["EmpresaUsuarioRol"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/permisos", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_nombres_empresa_usuario(db: Session = Depends(get_db)):
    return objRespuesta(
        respuesta=True,
        data=obtener_empresa_usuario_roles(db)
    )    

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def guardar_relacion(oCreate: EmpresaUsuarioRolCreate, db: Session = Depends(get_db)):
    return objRespuesta(
        respuesta = True,
        data = setEmpresaUsuario(db, oCreate.id_empresa, oCreate.id_usuario)
    )       


