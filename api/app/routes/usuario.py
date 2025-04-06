from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import true
from sqlalchemy.orm import Session
from app.schemas.respond import HTTPRespuesta
from app.database import SessionLocal
from app.schemas.usuario import UsuarioCreate, UsuarioOut,UsuarioLogin, UsuarioLoginRespuesta, UsuarioCambioPassword
from app.services.usuario import crear_usuario, validar_login_usuario, actualizar_password

router = APIRouter(tags=["Usuario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UsuarioOut, responses={400: {"model": HTTPRespuesta}})
def crear(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, usuario)



@router.get("/login", response_model=UsuarioLoginRespuesta, responses={400: {"model": HTTPRespuesta}})
def crear(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    """
    Inicia sesión de usuario si las credenciales son válidas.
    """
    respuesta = validar_login_usuario(db, usuario.userName, usuario.password)
    if respuesta:
        return respuesta
    # Si las credenciales no coinciden
    raise HTTPException(
        status_code=401,
        detail="Credenciales inválidas"
    )

# @router.put("/password", response_model=UsuarioLoginRespuesta, responses={400: {"model": HTTPRespuesta}})
# def cambiarPassword(usuario: UsuarioCambioPassword, db: Session = Depends(get_db)):
#     return actualizar_password(db,usuario.correo, usuario.userName, usuario.password)
