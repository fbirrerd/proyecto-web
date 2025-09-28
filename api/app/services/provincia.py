from typing import List
from sqlalchemy.orm import Session
from app.models.models import Provincia
from app.schemas.provincia import ProvinciaBase, ProvinciaCreate, ProvinciaUpdate

def get_all(db: Session) -> List[ProvinciaBase]:
    return db.query(Provincia).all()

def get_by_id(db: Session, item_id: int) -> ProvinciaBase:
    return db.query(Provincia).filter(Provincia.id == item_id).first()

def upsert(db: Session, item: ProvinciaCreate, item_id: int = None) -> ProvinciaBase:
    """
    Inserta una Provincia nueva o actualiza la existente si item_id está dado.
    """
    if item_id:
        db_item = db.query(Provincia).filter(Provincia.id == item_id).first()
        if db_item:
            # Actualizar campos
            for key, value in item.dict().items():
                setattr(db_item, key, value)
            db.commit()
            db.refresh(db_item)
            return db_item
        else:
            # No existe, crear uno nuevo con ese id
            new_item = Provincia(id=item_id, **item.dict())
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return new_item
    else:
        # Crear nuevo registro sin id especificado
        new_item = Provincia(**item.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

def delete(db: Session, item_id: int) -> ProvinciaBase:
    db_item = db.query(Provincia).filter(Provincia.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

def create(db: Session, modulo: ProvinciaCreate):
    data = Provincia(**modulo.dict())
    db.add(datos)
    db.commit()
    db.refresh(datos)
    return datos

def update(db: Session, modulo_id: int, modulo: ProvinciaUpdate) -> ProvinciaBase:
    data = get_by_id(db, modulo_id)
    if datos:
        for key, value in modulo.dict(exclude_unset=True).items():
            setattr(datos, key, value)
        db.commit()
        db.refresh(datos)
    return datos