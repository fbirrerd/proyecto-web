from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.empresaUsuario import EmpresaUsuarioCreate
from app.services.empresaUsuario import getDatosEmpresaUsuario, setEmpresaUsuario
from app.schemas.respond import objRespuesta
from app.database import SessionLocal

router = APIRouter(tags=["EmpresaUsuario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/list", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_nombres_empresa_usuario(db: Session = Depends(get_db)):
    try:
        datos = getDatosEmpresaUsuario(db)
        return objRespuesta(respuesta=True, data=datos)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al obtener datos: {str(e)}")

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def crear_relacion_empresa_usuario(oCreate: EmpresaUsuarioCreate, db: Session = Depends(get_db)):
    try:
        resultado = setEmpresaUsuario(db, oCreate)
        return objRespuesta(respuesta=True, data=resultado)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al guardar relación: {str(e)}")

@router.put("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def actualizar_relacion_empresa_usuario(oCreate: EmpresaUsuarioCreate, db: Session = Depends(get_db)):
    try:
        resultado = setEmpresaUsuario(db, oCreate)
        return objRespuesta(respuesta=True, data=resultado)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al actualizar relación: {str(e)}")
