from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.empresaUsuario import EmpresaUsuarioCreate
from app.services.empresaUsuario import getDatosEmpresaUsuario, setEmpresaUsuario
from app.schemas.respond import objRespuesta
from app.database import SessionLocal
from app.schemas.empresa import EmpresaCreate, EmpresaOut


router = APIRouter(tags=["EmpresaUsuario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/list", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_nombres_empresa_usuario(db: Session = Depends(get_db)):
    return objRespuesta(
        respuesta=True,
        data=getDatosEmpresaUsuario(db)
    )    

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def guardar_relacion(oCreate: EmpresaUsuarioCreate, db: Session = Depends(get_db)):
    return objRespuesta(
        respuesta = True,
        data = setEmpresaUsuario(oCreate, db)
    )    
