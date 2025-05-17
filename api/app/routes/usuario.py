from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.usuario import UsuarioCambioClave, UsuarioCambioEstado, UsuarioCreate, UsuarioUpdate
from app.services.usuario import (
    cambiar_clave,
    cambiar_estado,
    create_usuario,
    delete_usuario,
    get_lista,
    get_usuario,
    get_usuario_x_login,
    get_usuarios,
    update_usuario
)
from app.schemas.respond import objRespuesta
from app.database import SessionLocal

router = APIRouter(tags=["Usuario"])

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# ENDPOINT: Obtener lista ID-nombre de empresas
# -------------------------------
@router.get("/list/all", response_model=objRespuesta)
def obtener_lista_empresas(db: Session = Depends(get_db)):
    try:
        lista = get_lista(db)
        return objRespuesta(respuesta=True, data=lista)
    except Exception as e:
        return objRespuesta(
            respuesta=False,
            mensaje=f"Error al obtener la lista de empresas: {str(e)}",
            data=[]
        )

# -------------------------------
# ENDPOINT: Obtener usuario por login/username
# -------------------------------
@router.get("/login/{username}", response_model=objRespuesta)
def obtener_usuario_por_username(username: str, db: Session = Depends(get_db)):
    usuario = get_usuario_x_login(db, username)
    if not usuario:
        return objRespuesta(respuesta=False, data="Usuario no encontrado")
    return objRespuesta(respuesta=True, data=usuario)

# -------------------------------
# ENDPOINT: Listar todos los usuarios
# -------------------------------
@router.get("/", response_model=objRespuesta)
def listar_usuarios(db: Session = Depends(get_db)):
    try:
        usuarios = get_usuarios(db)
        return objRespuesta(respuesta=True, data=usuarios)
    except Exception as e:
        return objRespuesta(
            respuesta=False,
            data={"mensaje": f"Error al listar usuarios: {str(e)}"}
        )

# -------------------------------
# ENDPOINT: Obtener un usuario por ID
# -------------------------------
@router.get("/{usuario_id}", response_model=objRespuesta)
def obtener_usuario_por_id(usuario_id: int, db: Session = Depends(get_db)):
    usuario = get_usuario(db, usuario_id)
    if not usuario:
        return objRespuesta(respuesta=False, data="Usuario no encontrado")
    return objRespuesta(respuesta=True, data=usuario)

# -------------------------------
# ENDPOINT: Crear un nuevo usuario
# -------------------------------
@router.post("/", response_model=objRespuesta)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        result = create_usuario(db, usuario)
        return objRespuesta(respuesta=True, data=result)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al crear el usuario: {str(e)}")

# -------------------------------
# ENDPOINT: Actualizar un usuario
# -------------------------------
@router.put("/actualizar/{usuario_id}", response_model=objRespuesta)
def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    try:
        result = update_usuario(db, usuario_id, datos)
        if not result:
            return objRespuesta(respuesta=False, data="Usuario no encontrado")
        return objRespuesta(respuesta=True, data=result)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al actualizar el usuario: {str(e)}")

# -------------------------------
# ENDPOINT: Eliminar un usuario
# -------------------------------
@router.delete("/{usuario_id}", response_model=objRespuesta)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    result = delete_usuario(db, usuario_id)
    if not result:
        return objRespuesta(respuesta=False, data="Usuario no encontrado")
    return objRespuesta(respuesta=True, mensaje="Usuario eliminado", data=[])

# -------------------------------
# ENDPOINT: Cambiar estado del usuario
# -------------------------------
@router.put("/cambiar-estado", response_model=objRespuesta)
def cambiar_estado_usuario(obj: UsuarioCambioEstado, db: Session = Depends(get_db)):
    try:
        respuesta = cambiar_estado(db, obj)
        return objRespuesta(respuesta=True, data=respuesta)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al cambiar el estado: {str(e)}")

# -------------------------------
# ENDPOINT: Cambiar contraseña del usuario
# -------------------------------
@router.put("/cambiar-password", response_model=objRespuesta)
def cambiar_clave_usuario(obj: UsuarioCambioClave, db: Session = Depends(get_db)):
    try:
        respuesta = cambiar_clave(db, obj)
        return objRespuesta(respuesta=True, data=respuesta)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al cambiar la password: {str(e)}")
