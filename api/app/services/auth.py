from fastapi import Request
from app.services.logAcceso import registrar_log_acceso
from app.services.complejos import getObjetoAcceso
from app.schemas.auth import LoginReload, UsuarioCambioPassword, UsuarioLogin
from app.models.models import Acceso, EmpresaUsuario, Usuario
from app.utils.password import get_password_hash, verify_password
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from sqlalchemy import and_, or_
from app.schemas.respond import objRespuesta

# Función utilitaria para obtener IP y user-agent
def obtener_info_cliente(request: Request):
    if request:
        ip = request.client.host
        user_agent = request.headers.get("user-agent")
        return ip, user_agent
    return None, None

def validar_login_usuario(db: Session, user: UsuarioLogin, request: Request) -> objRespuesta:
    ip, user_agent = obtener_info_cliente(request)

    usuarioID = ""

    try:
        userObj = db.query(Usuario).filter(
            or_(Usuario.username == user.username, Usuario.email == user.username)
        ).first()

        if not userObj:
            registrar_log_acceso(db, userObj.username, False, "Usuario no encontrado", userObj.id, ip, user_agent)
            return objRespuesta(respuesta=False, data={'error': 'Usuario no existe en la base de datos'})
        
        usuarioID = userObj.id 

        if userObj.password == "cambiar":
            registrar_log_acceso(db, userObj.username, True, "Requiere cambio de clave", userObj.id, ip, user_agent)
            return objRespuesta(respuesta=True, data={'cambioClave': True})

        if not verify_password(user.password, userObj.password):
            registrar_log_acceso(db, userObj.username, False, "Contraseña incorrecta", userObj.id, ip, user_agent)
            return objRespuesta(respuesta=False, data={'error': 'Usuario y clave inválidos'})

        objAcceso = getObjetoAcceso(db, userObj.id)
        registrar_log_acceso(db, userObj.username, True, "Login exitoso", userObj.id, ip, user_agent)

        return objRespuesta(respuesta=True, data=objAcceso)

    except Exception as e:
        print(f"❌ Error durante la validación del login: {e}")
        registrar_log_acceso(db, user.username, False, f"Excepción en login: {e}", usuarioID, ip, user_agent)
        return objRespuesta(
            respuesta=False,
            data={'error': {"numero": 500, "mensaje": f'Ocurrió un error interno: {str(e)}'}}
        )


def validar_token_empresa(db: Session, login: LoginReload, request: Request) -> objRespuesta:
    try:
        ip, user_agent = obtener_info_cliente(request)
        # Buscar el usuario con el nombre de usuario proporcionado
        idUsuario = getIDUsuarioXToken(db, login.token)


        objAcceso = getObjetoAcceso(db, 
                                    idUsuario,
                                    login.empresaid, 
                                    login.token)
        registrar_log_acceso(db, objAcceso.username, True, "Cambio de empresa exitoso. Nueva empresa: " + login.empresaid, objAcceso.id, ip, user_agent)
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


def actualizar_password(db: Session, user: UsuarioCambioPassword, request: Request) -> objRespuesta:
    ip, user_agent = obtener_info_cliente(request)
    userObj = db.query(Usuario).filter(
        and_(
            Usuario.username == user.username,
            Usuario.email == user.email
        )
    ).first()

    if userObj:
        userObj.password = get_password_hash(user.password)
        userObj.fecha_modificacion = datetime.now(timezone.utc) # 👈 Asegura que se actualice la fecha
        registrar_log_acceso(db, userObj.username, True, "Cambio de clave exitoso", userObj.id, ip, user_agent)
        db.commit()
        db.refresh(userObj)

        return objRespuesta(
            respuesta=True,
            data={
                "username": userObj.username,
                "email": userObj.email,
                "fecha_modificacion": userObj.fecha_modificacion.isoformat(),
                "mensaje": "Cambio de clave OK"
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
        return accesoObj.id_usuario
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

