from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.schemas.auth import UsuarioLogin
from app.models.models import Usuario
from app.utils.password import get_password_hash
from app.schemas.usuario import (
    AccesoUsuario, UsuarioCambioClave, UsuarioCambioEstado,
    UsuarioCreate, UsuarioId, UsuarioList, UsuarioOut,
    UsuarioUpdate, UsuariosListado
)


# ===============================
# Helpers internos
# ===============================
def _get_usuario_by_id(db: Session, usuario_id: int) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def _get_usuario_by_username_or_email(db: Session, username_or_email: str) -> Optional[Usuario]:
    return db.query(Usuario).filter(
        or_(Usuario.username == username_or_email, Usuario.email == username_or_email)
    ).first()


# ===============================
# CRUD
# ===============================
def salvar_usuario(db: Session, usuario: UsuarioCreate) -> UsuarioOut:
    """
    Inserta un nuevo usuario o actualiza datos básicos si ya existe.
    """
    db_usuario = db.query(Usuario).filter(Usuario.username == usuario.username).first()

    if db_usuario:
        db_usuario.email = usuario.email
        db_usuario.duracion = usuario.duracion
    else:
        db_usuario = Usuario(
            username=usuario.username,
            email=usuario.email,
            password="cambiar",  # ⚠️ Podrías generar un random temporal
            duracion=usuario.duracion,
            estado=True
        )
        db.add(db_usuario)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def update_usuario(db: Session, usuario_id: int, data: UsuarioUpdate) -> Optional[UsuarioOut]:
    """
    Actualiza un usuario, aplicando hash si se cambia la contraseña.
    """
    db_usuario = _get_usuario_by_id(db, usuario_id)
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


def delete_usuario(db: Session, usuario_id: int) -> Optional[UsuarioOut]:
    """
    Elimina un usuario por ID.
    """
    usuario = _get_usuario_by_id(db, usuario_id)
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario


# ===============================
# Consultas de usuarios
# ===============================
def getDatosUsuario(db: Session, user: UsuarioLogin) -> Optional[AccesoUsuario]:
    """
    Retorna datos de usuario para login (por username o email).
    """
    user_record = _get_usuario_by_username_or_email(db, user.username)
    return AccesoUsuario.from_orm(user_record) if user_record else None


def getDatosUsuarioXID(db: Session, userid: int) -> Optional[UsuarioOut]:
    """
    Retorna datos de usuario por ID.
    """
    user_record = _get_usuario_by_id(db, userid)
    return UsuarioOut.from_orm(user_record) if user_record else None


def get_usuarios(db: Session) -> List[UsuariosListado]:
    """
    Retorna lista simplificada de usuarios.
    """
    usuarios = db.query(Usuario).all()
    return [
        UsuariosListado(
            id=u.id,
            username=u.username,
            email=u.email,
            estado=u.estado
        ) for u in usuarios
    ]


def get_usuario(db: Session, usuario_id: int) -> Optional[UsuarioOut]:
    """
    Retorna el detalle de un usuario por ID.
    """
    return _get_usuario_by_id(db, usuario_id)


def get_usuario_x_login(db: Session, username: str) -> Optional[UsuarioId]:
    """
    Retorna el ID de usuario según username.
    """
    dato = db.query(Usuario.id).filter(Usuario.username == username).first()
    return UsuarioId(id=dato.id) if dato else None


def get_lista(db: Session) -> List[UsuarioList]:
    """
    Retorna lista de usuarios activos (para selects).
    """
    data = db.query(
        Usuario.id,
        func.concat(Usuario.nombres, ' ', Usuario.apellidos).label("nombreCompleto")
    ).filter(Usuario.estado == True).all()

    return [UsuarioList(id=r.id, nombreCompleto=r.nombreCompleto) for r in data]


# ===============================
# Cambios de estado / seguridad
# ===============================
def cambiar_estado(db: Session, obj: UsuarioCambioEstado) -> Optional[UsuarioOut]:
    """
    Cambia el estado de un usuario (activo/inactivo).
    """
    db_usuario = _get_usuario_by_id(db, obj.id)
    if not db_usuario:
        return None

    db_usuario.estado = obj.estado
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def cambiar_clave(db: Session, obj: UsuarioCambioClave) -> Optional[UsuarioOut]:
    """
    Cambia la contraseña de un usuario (con hashing).
    """
    db_usuario = _get_usuario_by_id(db, obj.id)
    if not db_usuario:
        return None

    db_usuario.password = get_password_hash(obj.password)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario
