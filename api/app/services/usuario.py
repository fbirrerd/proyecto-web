from fastapi import HTTPException
from datetime import datetime, timezone
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.services.complejos import get_objeto_acceso
from app.schemas.respond import ApiRespuesta
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioLogin, UsuarioCambioPassword
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

# Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

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


# Inicialización del contexto de cifrado (ejemplo usando bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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