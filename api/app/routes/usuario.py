from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.usuario import UsuarioCreate, UsuarioOut,UsuarioLogin, UsuarioLoginRespuesta, UsuarioCambioPassword
from app.services.usuario import crear_usuario, validar_login_usuario, actualizar_password

router = APIRouter(prefix="/usuario", tags=["Usuario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UsuarioOut)
def crear(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, usuario)

@router.get("/login", response_model=UsuarioLoginRespuesta)
def crear(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    return validar_login_usuario(usuario.userName, usuario.password)

@router.put("/password", response_model=UsuarioLoginRespuesta)
def cambiarPassword(usuario: UsuarioCambioPassword, db: Session = Depends(get_db)):
    return actualizar_password(db,usuario.correo, usuario.userName, usuario.password)
