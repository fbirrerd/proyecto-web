from typing import List
from sqlalchemy.orm import Session
from app.models.models import Comuna, Provincia, Region
from app.schemas.comuna import ComunaBase, ComunaCreate, ComunaUpdate


def get_all(db: Session) -> List[ComunaBase]:
    return db.query(Comuna).all()

def get_by_id(db: Session, id_comuna: int) -> ComunaBase:
    return db.query(Comuna).filter(Comuna.id == id_comuna).first()

def get_by_id_provincia(db: Session, id_provincia: int) -> ComunaBase:
    return db.query(Comuna).filter(Comuna.id_provincia == id_provincia).first()

def upsert(db: Session, item: ComunaBase) -> ComunaBase:
    """
    Inserta una comuna nueva o actualiza la existente si item_id está dado.
    """
    db_item = db.query(Comuna).filter(Comuna.id == item.id).first()
    if db_item:
        # Actualizar campos
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return db_item
    else:
        # No existe, crear uno nuevo con ese id
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

def delete(db: Session, item_id: int) -> ComunaBase:
    db_item = db.query(Comuna).filter(Comuna.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

def create(db: Session, Comuna: ComunaCreate) -> ComunaBase:
    db_Comuna = Comuna(**Comuna.dict())
    db.add(db_Comuna)
    db.commit()
    db.refresh(db_Comuna)
    return db_Comuna

def update(db: Session, id_comuna: int, Comuna: ComunaUpdate) -> ComunaBase:
    db_Comuna = get_by_id(db, id_comuna)
    if db_Comuna:
        for key, value in Comuna.dict(exclude_unset=True).items():
            setattr(db_Comuna, key, value)
        db.commit()
        db.refresh(db_Comuna)
    return db_Comuna

def get_region_provincia_comuna_list(db: Session) -> ComunaBase:
    result = db.query(
        Region.id.label("id_region"),
        Region.nombre.label("nombre_region"),
        Provincia.id.label("id_provincia"),
        Provincia.nombre.label("nombre_provincia"),
        Comuna.id.label("id_comuna"),
        Comuna.nombre.label("nombre_comuna")
    ).join(Provincia, Provincia.id_region == Region.id
    ).join(Comuna, Comuna.id_provincia == Provincia.id
    ).all()

    # Convertir a lista de diccionarios
    listado = [
        {
            "id_region": row.id_region,
            "nombre_region": row.nombre_region,
            "id_provincia": row.id_provincia,
            "nombre_provincia": row.nombre_provincia,
            "id_comuna": row.id_comuna,
            "nombre_comuna": row.nombre_comuna,
        }
        for row in result
    ]

    return listado