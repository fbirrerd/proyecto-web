from sqlalchemy.orm import Session
from typing import List, Optional



# --- Propiedades Empresa ---
def create_propiedad_empresa(db: Session, payload: PropiedadEmpresaCreate) -> PropiedadEmpresa:
    obj = PropiedadEmpresa(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_propiedades_empresa(db: Session, empresa_id: Optional[int] = None):
    qry = db.query(PropiedadEmpresa)
    if empresa_id:
        qry = qry.filter(PropiedadEmpresa.empresa_id == empresa_id)
    return qry.all()

def get_propiedad_empresa(db: Session, id: int) -> Optional[PropiedadEmpresa]:
    return db.query(PropiedadEmpresa).filter(PropiedadEmpresa.id == id).first()

def update_propiedad_empresa(db: Session, id: int, payload: PropiedadEmpresaUpdate):
    obj = get_propiedad_empresa(db, id)
    if not obj:
        return None
    for k,v in payload.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete_propiedad_empresa(db: Session, id: int):
    obj = get_propiedad_empresa(db, id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
