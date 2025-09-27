from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VademecumOut(BaseModel):
    id_medicamento: int
    id_empresa: int
    url_logo: Optional[str] = None
    nombre_laboratorio: str
    url_medicamento: Optional[str] = None
    nombre_comercial: str
    nombre_generico: str
    forma_farmaceutica: str
    concentracion: str
    nombre_categoria: str
    estado: Optional[bool] = None
    fecha_creacion: datetime

    class Config:
        from_attributes = True  # permite mapear desde SQLAlchemy
