from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.empresaUsuario import AsignacionEmpresas, EmpresaUsuarioCreate
from app.services.empresaUsuario import generar_relaciones, getDatosEmpresaUsuario, getDatosEmpresaUsuario_idEmpresa, getDatosEmpresaUsuario_idUsuario, setEmpresaUsuario
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

@router.get("/empresa/{id_empresa}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def lista_empresausuario_empresa( id_empresa: int, db: Session = Depends(get_db)):
    try:
        datos = getDatosEmpresaUsuario_idEmpresa(id_empresa, db)
        return objRespuesta(respuesta=True, data=datos)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al obtener datos: {str(e)}")

@router.get("/usuario/{id_usuario}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def lista_empresausuario_usuario(id_usuario: int, db: Session = Depends(get_db)):
    try:
        datos = getDatosEmpresaUsuario_idUsuario(id_usuario, db)
        return objRespuesta(respuesta=True, data=datos)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al obtener datos: {str(e)}")

@router.post("/relacion-empresas")
def asignar_empresas(data: AsignacionEmpresas, db: Session = Depends(get_db)):
    try:
        datos = generar_relaciones(data, db)
        return objRespuesta(respuesta=True, data=datos)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al obtener datos: {str(e)}")
    