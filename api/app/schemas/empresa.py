from pydantic import BaseModel
from datetime import datetime

class EmpresaBase(BaseModel):
    nombre: str

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaOut(EmpresaBase):
    id: int
    fecha_creacion: datetime
    estado: int

    class Config:
        from_attributes = True
