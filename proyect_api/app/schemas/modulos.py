from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


class ModuloBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[bool] = True


class ModuloCreate(ModuloBase):
    pass


class ModuloUpdate(ModuloBase):
    pass


class ModuloInDB(ModuloBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        orm_mode = True
