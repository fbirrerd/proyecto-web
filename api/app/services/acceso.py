from sqlalchemy.orm import Session
from app.schemas.acceso import AccesoBase
from datetime import datetime, timedelta, timezone


def crear_usuario(db: Session, usuario: AccesoBase):
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

def create_acceso(db: Session, acceso: AccesoBase):

    db.add(acceso)
    db.commit()
    db.refresh(acceso)
    return acceso



def get_accesos(db: Session):
    return db.query(Acceso).all()

def get_acceso_by_id(db: Session, acceso_id: int):
    return db.query(Acceso).filter(Acceso.id == acceso_id).first()
