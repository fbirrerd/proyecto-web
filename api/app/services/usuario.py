from typing import List
from app.schemas.auth import UsuarioLogin
from app.models.models import Usuario
from app.utils.password import get_password_hash, verify_password
from app.schemas.usuario import UsuarioAcceso,  UsuarioCreate, UsuarioList, UsuarioOut, UsuarioUpdate
from sqlalchemy.orm import Session


from datetime import datetime, timezone
from sqlalchemy import and_, func, or_
from app.schemas.respond import objRespuesta

# Crear un nuevo usuario
def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(
        username=usuario.WWusername,
        nombres=usuario.nombres,
        apellidos=usuario.apellidos,
        email=usuario.email,
        password=usuario.password,  # Aquí debes usar hashing para la contraseña
        id_direccion=usuario.id_direccion,
        duracion=usuario.duracion,
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Obtener todos los usuarios
def get_all(db: Session):
    return db.query(Usuario).order_by(Usuario.nombre).all()

# Obtener un usuario por ID
def get_usuario(db: Session, id_usuario: int):
    return db.query(Usuario).filter(Usuario.id == id_usuario).first()

# Actualizar un usuario
def update_usuario(db: Session, id_usuario: int, usuario: UsuarioUpdate):
    db_usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
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
def delete_usuario(db: Session, id_usuario: int):
    db_usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
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
    
def get_usuarios(db: Session)  -> List[UsuarioOut]:
    return db.query(Usuario).all()

def get_usuario(db: Session, usuario_id: int) ->  UsuarioOut:
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def create_usuario(db: Session, usuario: UsuarioCreate) ->  UsuarioOut:
    db_usuario = Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, data: UsuarioUpdate) ->  UsuarioOut:
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(db_usuario, key, value)
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int) ->  UsuarioOut:
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario

def get_lista(db: Session) ->  UsuarioList:
    datos = db.query(
        Usuario.id,
        func.concat(Usuario.nombres, ' ', Usuario.apellidos).label("nombreCompleto")
    ).filter(Usuario.estado == True).all()

    return [UsuarioList(id=r.id, nombreCompleto=r.nombreCompleto) for r in datos]