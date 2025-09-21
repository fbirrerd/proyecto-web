from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from sqlalchemy import or_
from app.schemas.vademecum_medicamentos import MedicamentoCreate, MedicamentoUpdate
from app.utils.paginate import _paginate_list
from app.models.models import VademecumLaboratorio, VademecumCategoriaTerapeutica, VademecumMedicamento

from datetime import datetime

# ---------- Medicamentos ----------
def create_medicamento(db: Session, payload: MedicamentoCreate) -> VademecumMedicamento:
    obj = VademecumMedicamento(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_medicamento(db: Session, id_medicamento: int) -> Optional[VademecumMedicamento]:
    return db.query(VademecumMedicamento).filter(VademecumMedicamento.id_medicamento == id_medicamento).first()

def list_medicamentos(db: Session, id_empresa: Optional[int]=None, q: Optional[str]=None, page:int=1, per_page:int=10):
    qry = db.query(VademecumMedicamento)
    if id_empresa:
        qry = qry.filter(VademecumMedicamento.id_empresa == id_empresa)
    if q:
        like = f"%{q}%"
        qry = qry.filter(
            or_(
                VademecumMedicamento.nombre_comercial.ilike(like),
                VademecumMedicamento.nombre_generico.ilike(like)
            )
        )
    items, total = _paginate_list(qry.order_by(VademecumMedicamento.nombre_comercial), page, per_page)
    return items, total

def update_medicamento(db: Session, id_medicamento: int, payload: MedicamentoUpdate):
    obj = get_medicamento(db, id_medicamento)
    if not obj:
        return None
    for k,v in payload.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    obj.fecha_edicion = datetime.utcnow()
    db.commit()
    db.refresh(obj)
    return obj

def delete_medicamento(db: Session, id_medicamento: int):
    obj = get_medicamento(db, id_medicamento)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
