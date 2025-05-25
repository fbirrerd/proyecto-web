from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.schemas.auth import UsuarioLogin
from app.models.models import Usuario
from app.utils.password import get_password_hash, verify_password
from app.schemas.usuario import (
    UsuarioAcceso, UsuarioCambioClave, UsuarioCambioEstado,
    UsuarioCreate, UsuarioId, UsuarioList, UsuarioOut,
    UsuarioUpdate, UsuariosListado
)

# Crear o actualizar usuario
def salvar_usuario(db: Session, usuario: UsuarioCreate) -> UsuarioOut:
    db_usuario = db.query(Usuario).filter(Usuario.username == usuario.username).first()

    if db_usuario:
        # Actualiza campos
        db_usuario.nombres = usuario.nombres
        db_usuario.email = usuario.email
        db_usuario.duracion = usuario.duracion
    else:
        # Inserta nuevo
        db_usuario = Usuario(
            username=usuario.username,
            nombres=usuario.nombres,
            email=usuario.email,
            password="cambiar",
            duracion=usuario.duracion,
            estado=True
        )
        db.add(db_usuario)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


# Actualizar usuario, aplicando hashing si se cambia contraseña
def update_usuario(db: Session, usuario_id: int, data: UsuarioUpdate) -> Optional[UsuarioOut]:
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        return None

    update_data = data.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])

    for key, value in update_data.items():
        setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


# Eliminar usuario
def delete_usuario(db: Session, usuario_id: int) -> Optional[UsuarioOut]:
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario


# Login por username o email
def getDatosUsuario(db: Session, user: UsuarioLogin) -> Optional[UsuarioAcceso]:
    user_record = db.query(Usuario).filter(
        or_(Usuario.username == user.username, Usuario.email == user.username)
    ).first()
    return UsuarioAcceso.from_orm(user_record) if user_record else None


# Obtener usuario por ID (para acceso)
def getDatosUsuarioXID(db: Session, userid: int) -> Optional[UsuarioAcceso]:
    user_record = db.query(Usuario).filter(Usuario.id == userid).first()
    return UsuarioAcceso.from_orm(user_record) if user_record else None


# Listado de usuarios (simplificado)
def get_usuarios(db: Session) -> List[UsuariosListado]:
    lista = db.query(Usuario).all()
    return [
        UsuariosListado(
            id=o.id,
            username=o.username,
            nombres=f"{o.nombres} {o.apellidos}",
            email=o.email,
            estado=o.estado
        ) for o in lista
    ]


# Obtener usuario por ID (detalle)
def get_usuario(db: Session, usuario_id: int) -> Optional[UsuarioOut]:
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


# Obtener ID de usuario por username
def get_usuario_x_login(db: Session, username: str) -> Optional[UsuarioId]:
    dato = db.query(Usuario.id).filter(Usuario.username == username).first()
    return UsuarioId(id=dato.id) if dato else None


# Listado de usuarios activos para select (id + nombre completo)
def get_lista(db: Session) -> List[UsuarioList]:
    datos = db.query(
        Usuario.id,
        func.concat(Usuario.nombres, ' ', Usuario.apellidos).label("nombreCompleto")
    ).filter(Usuario.estado == True).all()

    return [UsuarioList(id=r.id, nombreCompleto=r.nombreCompleto) for r in datos]


# Cambiar estado del usuario
def cambiar_estado(db: Session, obj: UsuarioCambioEstado) -> Optional[UsuarioOut]:
    db_usuario = db.query(Usuario).filter(Usuario.id == obj.id).first()
    if not db_usuario:
        return None

    db_usuario.estado = obj.estado
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


# Cambiar contraseña del usuario
def cambiar_clave(db: Session, obj: UsuarioCambioClave) -> Optional[UsuarioOut]:
    db_usuario = db.query(Usuario).filter(Usuario.id == obj.id).first()
    if not db_usuario:
        return None

    db_usuario.password = get_password_hash(obj.password)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario
