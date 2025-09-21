from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from sqlalchemy import or_
from app.schemas.vademecum_categoria import CategoriaCreate, CategoriaUpdate
from app.utils.paginate import _paginate_list
from app.models.models import VademecumLaboratorio, VademecumCategoriaTerapeutica, VademecumMedicamento

from datetime import datetime

# ---------- Categorias ----------
def create_categoria(db: Session, payload: CategoriaCreate) -> VademecumCategoriaTerapeutica:
    obj = VademecumCategoriaTerapeutica(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_categoria(db: Session, id_categoria: int) -> Optional[VademecumCategoriaTerapeutica]:
    return db.query(VademecumCategoriaTerapeutica).filter(VademecumCategoriaTerapeutica.id_categoria == id_categoria).first()

def list_categorias(db: Session, id_empresa: Optional[int]=None, q: Optional[str]=None, page:int=1, per_page:int=10):
    qry = db.query(VademecumCategoriaTerapeutica)
    if id_empresa:
        qry = qry.filter(VademecumCategoriaTerapeutica.id_empresa == id_empresa)
    if q:
        like = f"%{q}%"
        qry = qry.filter(VademecumCategoriaTerapeutica.nombre_categoria.ilike(like))
    items, total = _paginate_list(qry.order_by(VademecumCategoriaTerapeutica.nombre_categoria), page, per_page)
    return items, total

def update_categoria(db: Session, id_categoria: int, payload: CategoriaUpdate):
    obj = get_categoria(db, id_categoria)
    if not obj:
        return None
    for k,v in payload.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    obj.fecha_edicion = datetime.utcnow()
    db.commit()
    db.refresh(obj)
    return obj

def delete_categoria(db: Session, id_categoria: int):
    obj = get_categoria(db, id_categoria)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
