from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AccesoBase(BaseModel):
    id_usuario: int
    id_empresa: Optional[int] = None
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