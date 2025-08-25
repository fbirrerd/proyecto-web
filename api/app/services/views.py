# app/queries/medicamentos.py
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.utils.redis_utils import get_redis
from typing import Optional
from typing import Optional, List
import json

def get_vademecum(db: Session, id_empresa: Optional[int] = None):
    print(f"pasa por aca")
    query = db.execute(text("SELECT * FROM vw_medicamentos_completos where id_empresa = " + id_empresa))
    medicamentos = [dict(row._mapping) for row in query]
    return medicamentos

# def get_vademecum_cache(db: Session, id_empresa: Optional[int] = None) -> List[Vademecum]:
#     redis_client = get_redis()
#     cache_key = f"vademecum:{id_empresa if id_empresa is not None else 'all'}"

#     # Intentar obtener datos del caché
#     cached_data = redis_client.get(cache_key)
#     if cached_data:
#         return [Vademecum(**item) for item in json.loads(cached_data)]

#     # Consultar la base de datos si no hay caché
#     query = db.query(Vademecum)
#     if id_empresa is not None:
#         query = query.filter(Vademecum.id_empresa == id_empresa)
#     vademecum = query.order_by(Vademecum.id_medicamento.asc()).all()

#     # Guardar en caché (serializar a JSON)
#     redis_client.setex(cache_key, 3600, json.dumps([item.__dict__ for item in vademecum]))

#     return vademecum