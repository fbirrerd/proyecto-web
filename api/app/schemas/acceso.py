from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AccesoBase(BaseModel):
    usuario_id: int
    empresa_id: Optional[int] = None
    fecha_vencimiento: datetime
    token: str

class AccesoCreate(AccesoBase):
    pass

class AccesoUpdate(AccesoBase):
    pass

class Acceso(AccesoBase):
    id: int
    fecha_ingreso: datetime
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        orm_mode = True