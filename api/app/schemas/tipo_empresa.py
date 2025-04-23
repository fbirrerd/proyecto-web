from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TipoEmpresaBase(BaseModel):
    nombre: Optional[str]
    estado: Optional[bool] = True

class TipoEmpresaCreate(TipoEmpresaBase):
    pass

class TipoEmpresaUpdate(TipoEmpresaBase):
    pass

class TipoEmpresaOut(TipoEmpresaBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        orm_mode = True

class TipoEmpresaList(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True