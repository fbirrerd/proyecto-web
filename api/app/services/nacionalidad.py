from typing import List
from sqlalchemy.orm import Session
from app.models.models import Nacionalidad
from app.schemas.nacionalidad import NacionalidadBase, NacionalidadCreate, NacionalidadUpdate

def get_all(db: Session) -> List[NacionalidadBase]:
    return db.query(Nacionalidad).all()

def get_by_id(db: Session, item_id: int) -> NacionalidadBase:
    return db.query(Nacionalidad).filter(Nacionalidad.id == item_id).first()

def upsert(db: Session, item: NacionalidadCreate, item_id: int = None) -> NacionalidadBase:
    """
    Inserta una Nacionalidad nueva o actualiza la existente si item_id está dado.
    """
    if item_id:
        db_item = db.query(Nacionalidad).filter(Nacionalidad.id == item_id).first()
        if db_item:
            # Actualizar campos
            for key, value in item.dict().items():
                setattr(db_item, key, value)
            db.commit()
            db.refresh(db_item)
            return db_item
        else:
            # No existe, crear uno nuevo con ese id
            new_item = Nacionalidad(id=item_id, **item.dict())
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return new_item
    else:
        # Crear nuevo registro sin id especificado
        new_item = Nacionalidad(**item.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

def delete(db: Session, item_id: int) -> NacionalidadBase:
    db_item = db.query(Nacionalidad).filter(Nacionalidad.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

def create(db: Session, modulo: NacionalidadCreate):
    db_nacionalidad = Nacionalidad(**modulo.dict())
    db.add(db_nacionalidad)
    db.commit()
    db.refresh(db_nacionalidad)
    return db_nacionalidad

def update(db: Session, id_modulo: int, modulo: NacionalidadUpdate) -> NacionalidadBase:
    db_nacionalidad = get_by_id(db, id_modulo)
    if db_nacionalidad:
        for key, value in modulo.dict(exclude_unset=True).items():
            setattr(db_nacionalidad, key, value)
        db.commit()
        db.refresh(db_nacionalidad)
    return db_nacionalidad