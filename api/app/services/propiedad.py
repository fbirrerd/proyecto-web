from sqlalchemy.orm import Session
from typing import List, Optional


# --- Propiedades ---
def create_propiedad(db: Session, payload: PropiedadCreate) -> Propiedad:
    obj = Propiedad(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_propiedades(db: Session):
    return db.query(Propiedad).all()

def get_propiedad(db: Session, id: int) -> Optional[Propiedad]:
    return db.query(Propiedad).filter(Propiedad.id == id).first()

def update_propiedad(db: Session, id: int, payload: PropiedadUpdate):
    obj = get_propiedad(db, id)
    if not obj:
        return None
    for k,v in payload.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete_propiedad(db: Session, id: int):
    obj = get_propiedad(db, id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


