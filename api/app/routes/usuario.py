from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.services.usuario import create_usuario, delete_usuario, get_lista, get_usuario, get_usuarios, update_usuario
from app.schemas.respond import objRespuesta
from app.database import SessionLocal

router = APIRouter(tags=["Usuario"])

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para listar usuarios
@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def listar_usuarios(db: Session = Depends(get_db)):
    try:
        usuarios = get_usuarios(db)
        return objRespuesta(
            respuesta=True,
            data=usuarios
        )
    except Exception as e:
        # Mejor manejo de la excepción con un mensaje detallado
        return objRespuesta(
            respuesta=False,
            mensaje=f"Error al listar usuarios: {str(e)}",  # Se pasa el mensaje de la excepción
            data=[]
        )

# Endpoint para obtener un usuario por ID
@router.get("/{usuario_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return objRespuesta(
        respuesta=True,
        data=usuario
    )

# Endpoint para crear un nuevo usuario
@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        result = create_usuario(db, usuario)
        return objRespuesta(
            respuesta=True,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear el usuario: {str(e)}")

# Endpoint para actualizar un usuario
@router.put("/{usuario_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    try:
        result = update_usuario(db, usuario_id, datos)
        if not result:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return objRespuesta(
            respuesta=True,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar el usuario: {str(e)}")

# Endpoint para eliminar un usuario
@router.delete("/{usuario_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    result = delete_usuario(db, usuario_id)
    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return objRespuesta(
        respuesta=True,
        mensaje="Usuario eliminado",
        data=[]
    )

# Endpoint para obtener una lista de empresas
@router.get("/list/all", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_id_nombre_empresas(db: Session = Depends(get_db)):
    try:
        lista = get_lista(db)
        return objRespuesta(
            respuesta=True,
            data=lista
        )
    except Exception as e:
        return objRespuesta(
            respuesta=False,
            mensaje=f"Error al obtener la lista de empresas: {str(e)}",
            data=[]
        )
