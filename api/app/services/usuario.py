from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioLogin, UsuarioCambioPassword, UsuarioLoginRespuesta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def crear_usuario(db: Session, usuario: UsuarioCreate):
    password = "cambia"
    db_usuario = Usuario(
        nombre_usuario=usuario.nombre_usuario,
        email=usuario.email,
        contrasena=password
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


# Inicialización del contexto de cifrado (ejemplo usando bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validar_login_usuario(db: Session, nombre_usuario: str, password: str) -> UsuarioLoginRespuesta:
    """
    Valida el login del usuario y verifica si necesita cambiar la contraseña.
    """
    # Buscar el usuario con el nombre de usuario proporcionado
    usuario = db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()

    # Si el usuario no existe, lanzar una excepción
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    # Validar si la contraseña necesita ser cambiada
    if usuario.contrasena == "cambiar":
        return UsuarioLoginRespuesta(
            respuesta=True,
            data={'cambioClave': True}
        )

    # La contraseña enviada es igual a  la contraseña enviada
    nueva_contrasena = get_password_hash(password)
    if not password == usuario.contrasena:  # Verificar la contraseña encriptada
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )



    # Si el usuario existe y la contraseña es correcta, devolvemos la respuesta con los datos del usuario
    return UsuarioLoginRespuesta(
        respuesta=True,
        data=usuario
    )



def actualizar_password(db: Session, correo: str, nombre_usuario: str, nueva_contrasena: str):
    # Buscar el usuario que coincida con el correo y el nombre de usuario
    usuario = db.query(Usuario).filter(
        and_(
            Usuario.email == correo,
            Usuario.nombre_usuario == nombre_usuario
        )
    ).first()  # Usamos .first() ya que solo esperamos un único registro
    
    if usuario:
        # Actualizar la contraseña
        usuario.contrasena = get_password_hash(nueva_contrasena)
        
        # Guardar los cambios en la base de datos
        db.commit()
        db.refresh(usuario)  # Opcional, para tener el objeto actualizado
        return usuario  # Retorna el usuario con la contraseña actualizada
    else:
        # Si no se encuentra el usuario, puedes devolver None o algún mensaje de error
        return None