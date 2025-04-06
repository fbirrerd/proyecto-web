from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AccesoBase(BaseModel):
    usuario_id: int
    empresa_id: Optional[int]
    fecha_vencimiento: datetime
    token: str


class AccesoValidar(AccesoBase):
    token: str
    
class AccesoOut(AccesoBase):
    id: int
    fecha_ingreso: datetime
    fecha_creacion: datetime
    fecha_modificacion: datetime
    class Config:
        from_attributes = True

