from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VademecumBase(BaseModel):
    url_logo: Optional[str] = None
    nombre_laboratorio: str
    id_medicamento: int
    url_medicamento: Optional[str] = None
    nombre_comercial: str
    nombre_generico: Optional[str] = None
    forma_farmaceutica: Optional[str] = None
    concentracion: Optional[str] = None
    nombre_categoria: Optional[str] = None
    estado: Optional[bool] = None
    fecha_creacion: Optional[datetime] = None
    id_empresa: int
