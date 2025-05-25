from sqlalchemy import true
from sqlalchemy.orm import Session

from app.models.models import LogAcceso


from sqlalchemy.orm import Session


import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Configuración básica del logger (ajústalo según tu proyecto)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def registrar_log_acceso(
    db: Session,
    username: str,
    exito: bool,
    mensaje: str,
    usuario_id: int = None,
    ip: str = None,
    user_agent: str = None
):
    print(f"registrar_log_acceso")
    try:        
        if not username:
            raise ValueError("El username no puede ser vacío.")
        if not mensaje:
            raise ValueError("El mensaje no puede ser vacío.")
        
        log = LogAcceso(
            username=username,
            exito=exito,
            mensaje=mensaje,
            ip=ip,
            user_agent=user_agent,
            id_usuario=usuario_id
        )
        print(log)
        db.add(log)
        db.commit()
        db.refresh(log)

        logger.info(
            f"LogAcceso registrado: username='{username}', exito={exito}, "
            f"id_usuario={usuario_id}, ip='{ip}', user_agent='{user_agent}', mensaje='{mensaje}'"
        )
        return log

    except (SQLAlchemyError, ValueError) as e:
        print(f"ERROR:   registrar_log_acceso")
        db.rollback()
        logger.error(f"Error al registrar log de acceso: {e}")
        return None
