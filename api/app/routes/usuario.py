from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import true
from sqlalchemy.orm import Session
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.services.usuario import create_usuario, delete_usuario, get_lista, get_usuario, get_usuarios, update_usuario
from app.schemas.respond import objRespuesta
from app.database import SessionLocal

router = APIRouter(tags=["Usuario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def listar_usuarios(db: Session = Depends(get_db)):
    return get_usuarios(db)

@router.get("/{usuario_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return create_usuario(db, usuario)

@router.put("/{usuario_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    return update_usuario(db, usuario_id, datos)

@router.delete("/{usuario_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    result = delete_usuario(db, usuario_id)
    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado"}


@router.get("/list/all", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_id_nombre_empresas(db: Session = Depends(get_db)):
    lista = get_lista(db)
    return objRespuesta(
        respuesta=True,
        data=lista
    )