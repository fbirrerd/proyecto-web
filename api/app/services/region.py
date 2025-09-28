from typing import List
from sqlalchemy.orm import Session
from app.models.models import Region
from app.schemas.region import RegionBase, RegionCreate, RegionUpdate

def get_all(db: Session) -> List[RegionBase]:
    return db.query(Region).all()

def get_by_id(db: Session, item_id: int) -> RegionBase:
    return db.query(Region).filter(Region.id == item_id).first()

def upsert(db: Session, item: RegionCreate, item_id: int = None) -> RegionBase:
    """
    Inserta una Region nueva o actualiza la existente si item_id está dado.
    """
    if item_id:
        db_item = db.query(Region).filter(Region.id == item_id).first()
        if db_item:
            # Actualizar campos
            for key, value in item.dict().items():
                setattr(db_item, key, value)
            db.commit()
            db.refresh(db_item)
            return db_item
        else:
            # No existe, crear uno nuevo con ese id
            new_item = Region(id=item_id, **item.dict())
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return new_item
    else:
        # Crear nuevo registro sin id especificado
        new_item = Region(**item.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

def delete(db: Session, item_id: int) -> RegionBase:
    db_item = db.query(Region).filter(Region.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

def create(db: Session, modulo: RegionCreate):
    data = Region(**modulo.dict())
    db.add(datos)
    db.commit()
    db.refresh(datos)

def update(db: Session, modulo_id: int, modulo: RegionUpdate) -> RegionBase:
    data = get_by_id(db, modulo_id)
    if datos:
        for key, value in modulo.dict(exclude_unset=True).items():
            setattr(datos, key, value)
        db.commit()
        db.refresh(datos)
    return datos