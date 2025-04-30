from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ModuloMenuBase(BaseModel):
    id_modulo: int
    id_menu: int
    estado: Optional[bool] = True


class ModuloMenuCreate(ModuloMenuBase):
    pass


class ModuloMenuUpdate(BaseModel):
    estado: Optional[bool]


class ModuloMenuInDB(ModuloMenuBase):
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        orm_mode = True
