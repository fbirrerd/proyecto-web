from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from sqlalchemy import or_
from app.schemas.vademecum_laboratorio import LaboratorioCreate, LaboratorioUpdate
from app.utils.paginate import _paginate_list
from app.models.models import VademecumLaboratorio, VademecumCategoriaTerapeutica, VademecumMedicamento

from datetime import datetime

# ---------- Laboratorios ----------
def create_laboratorio(db: Session, payload: LaboratorioCreate) -> VademecumLaboratorio:
    obj = VademecumLaboratorio(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_laboratorio(db: Session, id_laboratorio: int) -> Optional[VademecumLaboratorio]:
    return db.query(VademecumLaboratorio).filter(VademecumLaboratorio.id_laboratorio == id_laboratorio).first()

def list_laboratorios(db: Session, id_empresa: Optional[int]=None, q: Optional[str]=None, page:int=1, per_page:int=10):
    qry = db.query(VademecumLaboratorio)
    if id_empresa:
        qry = qry.filter(VademecumLaboratorio.id_empresa == id_empresa)
    if q:
        like = f"%{q}%"
        qry = qry.filter(or_(VademecumLaboratorio.nombre_laboratorio.ilike(like), VademecumLaboratorio.pais.ilike(like)))
    items, total = _paginate_list(qry.order_by(VademecumLaboratorio.nombre_laboratorio), page, per_page)
    return items, total

def update_laboratorio(db: Session, id_laboratorio: int, payload: LaboratorioUpdate):
    obj = get_laboratorio(db, id_laboratorio)
    if not obj:
        return None
    for k,v in payload.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    obj.fecha_edicion = datetime.utcnow()
    db.commit()
    db.refresh(obj)
    return obj

def delete_laboratorio(db: Session, id_laboratorio: int):
    obj = get_laboratorio(db, id_laboratorio)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
