from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import true
from sqlalchemy.orm import Session
from app.schemas.respond import ApiRespuesta
from app.database import SessionLocal
from app.schemas.usuario import UsuarioCreate, UsuarioOut,UsuarioLogin, UsuarioCambioPassword
from app.services.usuario import crear_usuario, validar_login_usuario, actualizar_password

router = APIRouter(tags=["Usuario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UsuarioOut, responses={400: {"model": ApiRespuesta}})
def crear(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, usuario)



@router.post("/login", response_model=ApiRespuesta, responses={400: {"model": ApiRespuesta}})
def crear(user: UsuarioLogin, db: Session = Depends(get_db)):
    """
    Inicia sesión de usuario si las credenciales son válidas.
    """
    respuesta = validar_login_usuario(db, user)
    if respuesta:
        return respuesta
    # Si las credenciales no coinciden
    return ApiRespuesta(
        respuesta=False,
        status_code=401,
        error="Problema con las credenciales"
    )
@router.put("/password", response_model=ApiRespuesta, responses={400: {"model": ApiRespuesta}})
def cambiarPassword(user: UsuarioCambioPassword, db: Session = Depends(get_db)):
    respuesta = actualizar_password(db, user)
    if respuesta:
        return respuesta
    # Si las credenciales no coinciden
    return ApiRespuesta(
        respuesta=False,
        status_code=401,
        error="Problema al actualizar la clave"
    )    

