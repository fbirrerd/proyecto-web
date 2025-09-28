from sqlalchemy.orm import Session
from app.models.models import Direccion
from schemas.direccion import DireccionCreate, DireccionUpdate
from fastapi import HTTPException

def get_direccion(db: Session, direccion_id: int):
    direccion = db.query(Direccion).filter(Direccion.id == direccion_id).first()
    if not direccion:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    return direccion

def create_direccion(db: Session, data: DireccionCreate):
    nueva = Direccion(**data.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def update_direccion(db: Session, direccion_id: int, data: DireccionUpdate):
    direccion = get_direccion(db, direccion_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(direccion, key, value)
    db.commit()
    db.refresh(direccion)
    return direccion
