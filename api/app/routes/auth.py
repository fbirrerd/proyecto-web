from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import true
from sqlalchemy.orm import Session
from app.schemas.auth import LoginReload, UsuarioCambioPassword, UsuarioLogin
from app.schemas.respond import objRespuesta
from app.database import SessionLocal
from app.services.auth import validar_login_usuario, actualizar_password, validar_token_empresa

router = APIRouter(tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    
@router.put("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def cambiarPassword(user: UsuarioCambioPassword, db: Session = Depends(get_db)):
    respuesta = actualizar_password(db, user)
    if respuesta:
        return respuesta
    # Si las credenciales no coinciden
    return objRespuesta(
        respuesta=False,
        data={"numero":401, "mensaje":"Problema al actualizar la clave"}
    )    


@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def crear(user: UsuarioLogin, db: Session = Depends(get_db)):
    respuesta = validar_login_usuario(db, user)
    if respuesta:
        return respuesta
    # Si las credenciales no coinciden
    return objRespuesta(
        respuesta=False,
        status_code=401,
        error="Problema con las credenciales"
    )
    
    
@router.post("/reload", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def crear(login: LoginReload, db: Session = Depends(get_db)):
    respuesta =  validar_token_empresa(db, login)
    if respuesta:
        return respuesta
    # Si las credenciales no coinciden
    return objRespuesta(
        respuesta=False,
        status_code=401,
        error="Problema con la validación del Token"
    )
       