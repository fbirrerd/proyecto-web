from app.services.complejos import getObjetoAcceso
from app.schemas.auth import LoginReload, UsuarioCambioPassword, UsuarioLogin
from app.models.models import Acceso, Usuario
from app.utils.password import get_password_hash, verify_password
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from sqlalchemy import and_, or_
from app.schemas.respond import objRespuesta

def validar_login_usuario(db: Session, user: UsuarioLogin) -> objRespuesta:
    try:
        # Buscar el usuario con el nombre de usuario proporcionado
        userObj = db.query(Usuario).filter(
            or_(Usuario.username == user.username,
                Usuario.email == user.username)
        ).first()

        # Si el usuario no existe, retornar respuesta de error
        if not userObj:
            return objRespuesta(
                respuesta=False,
                data={'error': 'Usuario no existe en la base de datos'}
            )

        # Validar si la contraseña necesita ser cambiada
        if userObj.password == "cambiar":
            return objRespuesta(
                respuesta=True,
                data={'cambioClave': True}
            )

        # Verificar si la contraseña proporcionada coincide con la almacenada
        if not verify_password(user.password, userObj.password):
            return objRespuesta(
                respuesta=False,
                data={'error': 'Usuario y clave inválidos'}
            )

        # Armar el objeto de acceso (si está implementado)
        objAcceso = getObjetoAcceso(db, userObj.id)

        # Si el usuario existe y la contraseña es correcta, retornar respuesta exitosa
        return objRespuesta(
            respuesta=True,
            data=objAcceso
        )

    except Exception as e:
        # Capturar cualquier excepción que ocurra durante el proceso
        print(f"Error durante la validación del login: {e}")
        return objRespuesta(
            respuesta=False,
            data={'error': {"numero": 500, "mensaje": f'Ocurrió un error interno: {e}'}}
        )

def validar_token_empresa(db: Session, login: LoginReload) -> objRespuesta:
    try:
        # Buscar el usuario con el nombre de usuario proporcionado
        idUsuario = getIDUsuarioXToken(db, login.token)


        objAcceso = getObjetoAcceso(db, idUsuario,
                                    login.empresaid, 
                                    login.token)

        # Si el usuario existe y la contraseña es correcta, retornar respuesta exitosa
        return objRespuesta(
            respuesta=True,
            data=objAcceso
        )

    except Exception as e:
        # Capturar cualquier excepción que ocurra durante el proceso
        return objRespuesta(
            respuesta=False,
            data={'error': {"numero": 500, "mensaje": f'Ocurrió un error interno: {e}'}}
        )


def actualizar_password(db: Session, user: UsuarioCambioPassword) -> objRespuesta:
    userObj = db.query(Usuario).filter(
        and_(
            Usuario.username == user.username,
            Usuario.email == user.email
        )
    ).first()

    if userObj:
        userObj.password = get_password_hash(user.password)
        userObj.fecha_modificacion = datetime.now(timezone.utc) # 👈 Asegura que se actualice la fecha

        db.commit()
        db.refresh(userObj)

        return objRespuesta(
            respuesta=True,
            data={
                "id": userObj.id,
                "username": userObj.username,
                "email": userObj.email,
                "fecha_modificacion": userObj.fecha_modificacion.isoformat()
            }
        )
    else:
        return objRespuesta(
            respuesta=False,
            error='No se encuentra el usuario',
            status_code=401
        )
        
        
def getIDUsuarioXToken(db: Session, token: str):
    accesoObj = db.query(Acceso).filter(
            Acceso.token == token
    ).first()

    if accesoObj:
        # Convierte el ORM en Pydantic
        return accesoObj.usuario_id
    else:
        return None       
    
# def recargarInfoUsuarioConectado(db: Session, userId: int, empresaId: int) -> objRespuesta:
#     try:
#         # Buscar el usuario con el nombre de usuario proporcionado
#         userObj = db.query(Usuario).filter(Usuario.id == userId).first()

#         # Si el usuario no existe, retornar respuesta de error
#         if not userObj:
#             return objRespuesta(
#                 respuesta=False,
#                 data={'error': 'Usuario no existe en la base de datos'}
#             )


#         # Armar el objeto de acceso (si está implementado)
#         objAcceso = getObjetoAcceso(db, userObj.id, empresaId)

#         # Si el usuario existe y la contraseña es correcta, retornar respuesta exitosa
#         return objRespuesta(
#             respuesta=True,
#             data=objAcceso
#         )

#     except Exception as e:
#         # Capturar cualquier excepción que ocurra durante el proceso
#         print(f"Error durante la recarga de datos dhasboard: {e}")
#         return objRespuesta(
#             respuesta=False,
#             data={'error': {"numero": 500, "mensaje": f'Ocurrió un error interno: {e}'}}
#         )

