import logging
from fastapi import Request
from app.services.logAcceso import registrar_log_acceso
from app.services.complejos import getObjetoAcceso
from app.schemas.auth import LoginReload, UsuarioCambioPassword, UsuarioLogin
from app.models.models import Acceso, Usuario
from app.utils.password import get_password_hash, verify_password
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from sqlalchemy import and_, or_
from app.schemas.respond import objRespuesta
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

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
    """
    Valida el token de empresa y registra el acceso.

    Args:
        db (Session): Sesión de base de datos.
        login (LoginReload): Objeto con datos de login (incluye token y empresaid).
        request (Request): Objeto de solicitud para obtener IP y user-agent.

    Returns:
        objRespuesta: Respuesta estructurada con éxito o error.
    """
    try:
        # Obtener datos del cliente
        ip, user_agent = obtener_info_cliente(request)

        # Obtener ID del usuario a partir del token
        id_usuario = getIDUsuarioXToken(db, login.token)
        if not id_usuario:
            logger.warning(f"Token inválido: {login.token}")
            return objRespuesta(
                respuesta=False,
                data={'error': {"numero": 401, "mensaje": "Token inválido"}}
            )

        # Obtener objeto de acceso con permisos/empresa
        obj_acceso = getObjetoAcceso(db, id_usuario, login.empresaid, login.token)
        if not obj_acceso:
            logger.warning(f"Acceso denegado: id_usuario={id_usuario}, empresaid={login.empresaid}")
            return objRespuesta(
                respuesta=False,
                data={'error': {"numero": 403, "mensaje": "Acceso denegado a la empresa"}}
            )

        # Registrar el log de acceso exitoso
        mensaje_log = f"Cambio de empresa exitoso. Nueva empresa: {login.empresaid}"
        registrar_log_acceso(
            db,
            username=obj_acceso.username,
            exito=True,
            mensaje=mensaje_log,
            usuario_id=obj_acceso.usuario.id,
            ip=ip,
            user_agent=user_agent
        )
        logger.info(f"Usuario {obj_acceso.username} cambió exitosamente a empresa {login.empresaid}")

        return objRespuesta(
            respuesta=True,
            data=obj_acceso
        )

    except Exception as e:
        logger.exception(f"Error al validar token de empresa: {e}")
        return objRespuesta(
            respuesta=False,
            data={'error': {"numero": 500, "mensaje": "Ocurrió un error interno. Contacte al administrador."}}
        )
def actualizar_password(db: Session, user: UsuarioCambioPassword, request: Request) -> objRespuesta:
    ip, user_agent = obtener_info_cliente(request)

    # Validar datos básicos
    if not user.username or not user.email or not user.password:
        return objRespuesta(
            respuesta=False,
            error='Faltan datos obligatorios (username, email o password)',
            status_code=400
        )

    try:
        userObj = db.query(Usuario).filter(
            Usuario.username == user.username,
            Usuario.email == user.email
        ).first()

        if not userObj:
            return objRespuesta(
                respuesta=False,
                error='No se encuentra el usuario',
                status_code=404
            )

        # Actualizar contraseña y fecha
        userObj.password = get_password_hash(user.password)
        userObj.fecha_modificacion = datetime.now(timezone.utc)

        # Guardar cambios
        db.commit()
        db.refresh(userObj)

        # Registrar log
        registrar_log_acceso(db,userObj.username,True,"Cambio de clave exitoso",userObj.id,ip,user_agent)

        return objRespuesta(
            respuesta=True,
            data={
                "username": userObj.username,
                "email": userObj.email,
                "fecha_modificacion": userObj.fecha_modificacion.isoformat(),
                "mensaje": "Cambio de clave OK"
            }
        )

    except SQLAlchemyError as e:
        db.rollback()
        print(f"error ....: {str(e)}")
        registrar_log_acceso(db,user.username,False,f"Error al cambiar clave: {str(e)}",None,ip,user_agent)
        return objRespuesta(
            respuesta=False,
            error='Error interno al intentar cambiar la clave',
            status_code=500
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
