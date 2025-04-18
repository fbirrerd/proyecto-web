from sqlalchemy import true
from sqlalchemy.orm import Session

from app.models.models import LogAcceso


def registrar_log_acceso(db, username: str, exito: bool, mensaje: str, id_usuario: int, ip: str, user_agent: str):
    try:
        log = LogAcceso(
            id_usuario=id_usuario,
            username=username,
            exito=exito,
            mensaje=mensaje,
            ip=ip,
            user_agent=user_agent
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    except Exception as e:
        db.rollback()
        print("❌ Error registrando el log de acceso:", str(e))