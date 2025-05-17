from sqlalchemy import true
from sqlalchemy.orm import Session

from app.models.models import LogAcceso


from sqlalchemy.orm import Session


def registrar_log_acceso(
    db: Session,
    username: str,
    exito: bool,
    mensaje: str,
    usuario_id: int = None,
    ip: str = None,
    user_agent: str = None
):
    log = LogAcceso(
        username=username,
        exito=exito,
        mensaje=mensaje,
        ip=ip,
        user_agent=user_agent,
        id_usuario=usuario_id
    )

    # Forma recomendada para depurar: mostrar los atributos clave
    print(f"log creado: username={log.username}, exito={log.exito}, mensaje={log.mensaje}, ip={log.ip}, user_agent={log.user_agent}, id_usuario={log.id_usuario}")

    db.add(log)
    db.commit()
    db.refresh(log)
    return log