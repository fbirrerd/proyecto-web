from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class EmpresaModuloBase(BaseModel):
    id_empresa: int
    id_modulo: int
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    estado: Optional[bool] = True


class EmpresaModuloCreate(EmpresaModuloBase):
    pass


class EmpresaModuloUpdate(BaseModel):
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]
    estado: Optional[bool]


class EmpresaModuloOut(EmpresaModuloBase):
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        orm_mode = True

class EmpresaModuloInDB(EmpresaModuloBase):
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        orm_mode = True

class EmpresaModuloOut(EmpresaModuloBase):
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        orm_mode = True
