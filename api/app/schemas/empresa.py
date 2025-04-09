from typing import Optional
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



class EmpresaAcceso(EmpresaBase):
    id: int    
    nombre: str
    tipo_empresa: str
    direccion_id: Optional[int] = None    

    class Config:
        orm_mode = True