from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.schemas.auth import UsuarioLogin
from app.models.models import Usuario
from app.utils.password import get_password_hash, verify_password
from app.schemas.usuario import UsuarioAcceso, UsuarioCambioClave, UsuarioCambioEstado, UsuarioCreate, UsuarioId, UsuarioList, UsuarioOut, UsuarioUpdate, UsuariosListado

# Crear un nuevo usuario con password hasheada
def create_usuario(db: Session, usuario: UsuarioCreate) -> UsuarioOut:
    hashed_password = get_password_hash(usuario.password)
    db_usuario = Usuario(
        username=usuario.username,
        nombres=usuario.nombres,
        apellidos=usuario.apellidos,
        email=usuario.email,
        password=hashed_password,
        id_direccion=usuario.id_direccion,
        duracion=usuario.duracion,
        estado=True  # Suponiendo que es activo por defecto
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Actualizar usuario, aplicando hashing si se actualiza password
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

# Eliminar un usuario
def delete_usuario(db: Session, usuario_id: int) -> Optional[UsuarioOut]:
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario

# Obtener datos de usuario a partir de username o email (login)
def getDatosUsuario(db: Session, user: UsuarioLogin) -> Optional[UsuarioAcceso]:
    user_record = db.query(Usuario).filter(
        or_(Usuario.username == user.username, Usuario.email == user.username)
    ).first()
    if user_record:
        return UsuarioAcceso.from_orm(user_record)
    return None

# Obtener datos de usuario por ID
def getDatosUsuarioXID(db: Session, userid: int) -> Optional[UsuarioAcceso]:
    user_record = db.query(Usuario).filter(Usuario.id == userid).first()
    if user_record:
        return UsuarioAcceso.from_orm(user_record)
    return None

# Listar usuarios (con formato simplificado)
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

# Obtener usuario por ID (objeto único, no lista)
def get_usuario(db: Session, usuario_id: int) -> Optional[UsuarioOut]:
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        return usuario
    return None

# Obtener usuario por username (objeto único)
def get_usuario_x_login(db: Session, username: str) -> UsuarioId:
    dato = db.query(Usuario.id).filter(Usuario.username == username).first()
    if dato:
        return UsuarioId(id=dato.id)
    else:
        return None  # o lanza excepción si prefieres
    
    
# Obtener lista simplificada de usuarios activos para select (ID + nombre completo)
def get_lista(db: Session) -> List[UsuarioList]:
    datos = db.query(
        Usuario.id,
        func.concat(Usuario.nombres, ' ', Usuario.apellidos).label("nombreCompleto")
    ).filter(Usuario.estado == True).all()

    return [UsuarioList(id=r.id, nombreCompleto=r.nombreCompleto) for r in datos]

# cambiar estado
def cambiar_estado(db: Session, obj: UsuarioCambioEstado) -> Optional[UsuarioOut]:
    db_usuario = db.query(Usuario).filter(Usuario.id == obj.id).first()
    if not db_usuario:
        return None

    db_usuario.estado = obj.estado

    db.commit()
    db.refresh(db_usuario)
    return db_usuario
    
# cambiar clave
def cambiar_clave(db: Session, obj: UsuarioCambioClave) -> Optional[UsuarioOut]:
    db_usuario = db.query(Usuario).filter(Usuario.id == obj.id).first()
    if not db_usuario:
        return None

    db_usuario.password = get_password_hash(obj.password)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario
        
    