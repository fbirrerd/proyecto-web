# app/crud/usuario.py
from app.utils.password import get_password_hash, verify_password
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioLogin, UsuarioCambioPassword, UsuarioUpdate
from sqlalchemy.orm import Session
from app.services.complejos import get_objeto_acceso

from datetime import datetime, timezone
from sqlalchemy import and_, or_
from app.schemas.respond import ApiRespuesta

# Crear un nuevo usuario
def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(
        username=usuario.username,
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
        nombre_usuario=usuario.nombre_usuario,
        email=usuario.email,
        contrasena=password,
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def validar_login_usuario(db: Session, user: UsuarioLogin) -> ApiRespuesta:
    # Buscar el usuario con el nombre de usuario proporcionado
    userObj = db.query(Usuario).filter(
        or_(Usuario.nombre_usuario == user.userName, 
            Usuario.email == user.userName)
    ).first()

    # Si el usuario no existe, lanzar una excepción
    if not userObj:
        return ApiRespuesta(
            respuesta=False,
            data={'error': 'Usuario no existe en la base de datos'}
        )

    # Validar si la contraseña necesita ser cambiada
    if userObj.contrasena == "cambiar":
        return ApiRespuesta(
            respuesta=True,
            data={'cambioClave': True}
        )

    # La contraseña enviada es igual a  la contraseña enviada
    if not verify_password(user.password, userObj.contrasena):
        return ApiRespuesta(
            respuesta=False,
            data={
                'error': 'Usuario y clave inválidos'}
        )

    # Armamos el nuevo objeto gigante
    objAcceso = get_objeto_acceso(db, user)
    # Si el usuario existe y la contraseña es correcta, devolvemos la respuesta con los datos del usuario
    return ApiRespuesta(
        respuesta=True,
        data=objAcceso
    )



def actualizar_password(db: Session, user: UsuarioCambioPassword) -> ApiRespuesta:
    userObj = db.query(Usuario).filter(
        and_(
            Usuario.nombre_usuario == user.userName,
            Usuario.email == user.email
        )
    ).first()

    if userObj:
        userObj.contrasena = get_password_hash(user.password)
        userObj.fecha_modificacion = datetime.now(timezone.utc) # 👈 Asegura que se actualice la fecha

        db.commit()
        db.refresh(userObj)

        return ApiRespuesta(
            respuesta=True,
            data={
                "id": userObj.id,
                "nombre_usuario": userObj.nombre_usuario,
                "email": userObj.email,
                "fecha_modificacion": userObj.fecha_modificacion.isoformat()
            }
        )
    else:
        return ApiRespuesta(
            respuesta=False,
            error='No se encuentra el usuario',
            status_code=401
        )