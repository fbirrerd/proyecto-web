from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioLogin, UsuarioCambioPassword
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


def validar_login_usuario(db: Session, nombre_usuario: str, password: str) -> bool:
    # Buscar el usuario con el nombre de usuario y la contraseña proporcionada
    usuario = db.query(Usuario).filter(
        and_(
            Usuario.nombre_usuario == nombre_usuario,
            Usuario.contrasena == password
        )
    ).first()  # .first() devuelve el primer registro o None si no existe

    # Si el usuario existe, retornamos True, de lo contrario False
    return usuario is not None



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