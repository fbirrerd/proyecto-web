from typing import List
from sqlalchemy.orm import Session
from app.models.models import EstadoCivil
from app.schemas.estadoCivil import EstadoCivilBase, EstadoCivilCreate, EstadoCivilUpdate

def get_all(db: Session) -> List[EstadoCivilBase]:
    return db.query(EstadoCivil).all()

def get_by_id(db: Session, item_id: int) -> EstadoCivilBase:
    return db.query(EstadoCivil).filter(EstadoCivil.id == item_id).first()

def upsert(db: Session, item: EstadoCivilCreate, item_id: int = None) -> EstadoCivilBase:
    """
    Inserta una EstadoCivil nueva o actualiza la existente si item_id está dado.
    """
    if item_id:
        db_item = db.query(EstadoCivil).filter(EstadoCivil.id == item_id).first()
        if db_item:
            # Actualizar campos
            for key, value in item.dict().items():
                setattr(db_item, key, value)
            db.commit()
            db.refresh(db_item)
            return db_item
        else:
            # No existe, crear uno nuevo con ese id
            new_item = EstadoCivil(id=item_id, **item.dict())
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return new_item
    else:
        # Crear nuevo registro sin id especificado
        new_item = EstadoCivil(**item.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

def delete(db: Session, item_id: int) -> EstadoCivilBase:
    db_item = db.query(EstadoCivil).filter(EstadoCivil.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

def create(db: Session, modulo: EstadoCivilCreate) -> EstadoCivilBase:
    db_modulo = EstadoCivil(**modulo.dict())
    db.add(db_modulo)
    db.commit()
    db.refresh(db_modulo)
    return db_modulo

def update(db: Session, modulo_id: int, modulo: EstadoCivilUpdate) -> EstadoCivilBase:
    db_modulo = get_by_id(db, modulo_id)
    if db_modulo:
        for key, value in modulo.dict(exclude_unset=True).items():
            setattr(db_modulo, key, value)
        db.commit()
        db.refresh(db_modulo)
    return db_modulo