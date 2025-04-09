from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas.acceso import AccesoCreate, AccesoUpdate
from app.models.models import Acceso

def obtener_acceso(db: Session, acceso_id: int):
    return db.query(Acceso).filter(Acceso.id == acceso_id).first()

def obtener_todos_los_accesos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Acceso).offset(skip).limit(limit).all()

def crear_acceso(db: Session, acceso: AccesoCreate):
    nuevo_acceso = Acceso(
        usuario_id=acceso.usuario_id,
        empresa_id=acceso.empresa_id,
        fecha_vencimiento=acceso.fecha_vencimiento,
        token=acceso.token,
    )
    db.add(nuevo_acceso)
    db.commit()
    db.refresh(nuevo_acceso)
    return nuevo_acceso

def actualizar_acceso(db: Session, acceso_id: int, acceso_actualizado: AccesoUpdate):
    acceso = db.query(Acceso).filter(Acceso.id == acceso_id).first()
    if acceso:
        acceso.usuario_id = acceso_actualizado.usuario_id
        acceso.empresa_id = acceso_actualizado.empresa_id
        acceso.fecha_vencimiento = acceso_actualizado.fecha_vencimiento
        acceso.token = acceso_actualizado.token
        acceso.fecha_modificacion = datetime.now()
        db.commit()
        db.refresh(acceso)
    return acceso

def eliminar_acceso(db: Session, acceso_id: int):
    acceso = db.query(Acceso).filter(Acceso.id == acceso_id).first()
    if acceso:
        db.delete(acceso)
        db.commit()
    return acceso
