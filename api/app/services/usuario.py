from app.schemas.auth import UsuarioLogin
from app.models.models import Usuario
from app.utils.password import get_password_hash, verify_password
from app.schemas.usuario import UsuarioAcceso,  UsuarioCreate, UsuarioUpdate
from sqlalchemy.orm import Session


from datetime import datetime, timezone
from sqlalchemy import and_, or_
from app.schemas.respond import objRespuesta

# Crear un nuevo usuario
def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(
        username=usuario.WWusername,
        nombres=usuario.nombres,
        apellidos=usuario.apellidos,
        email=usuario.email,
        password=usuario.password,  # Aquí debes usar hashing para la contraseña
        direccion_id=usuario.direccion_id,
        duracion=usuario.duracion,
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Obtener todos los usuarios
def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Usuario).offset(skip).limit(limit).all()

# Obtener un usuario por ID
def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

# Actualizar un usuario
def update_usuario(db: Session, usuario_id: int, usuario: UsuarioUpdate):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario:
        if usuario.username:
            db_usuario.username = usuario.username
        if usuario.nombres:
            db_usuario.nombres = usuario.nombres
        if usuario.apellidos:
            db_usuario.apellidos = usuario.apellidos
        if usuario.email:
            db_usuario.email = usuario.email
        if usuario.password:
            db_usuario.password = usuario.password
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

# Eliminar un usuario
def delete_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return db_usuario


def crear_usuario(db: Session, usuario: UsuarioCreate):
    password = "cambiar"
    db_usuario = Usuario(
        username=usuario.username,
        email=usuario.email,
        password=password,
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def getDatosUsuario(db: Session, user: UsuarioLogin):
    userList = db.query(Usuario).filter(
        or_(Usuario.username == user.username, 
            Usuario.email == user.username)
        ).first()
 
    if userList:
        # Convierte el ORM en Pydantic
        usuario_pydantic = UsuarioAcceso.from_orm(userList)
        return usuario_pydantic
    else:
        return None   
    
def getDatosUsuarioXID(db: Session, userid: int):
    userList = db.query(Usuario).filter(Usuario.id == userid).first()
 
    if userList:
        # Convierte el ORM en Pydantic
        usuario_pydantic = UsuarioAcceso.from_orm(userList)
        return usuario_pydantic
    else:
        return None   
    
