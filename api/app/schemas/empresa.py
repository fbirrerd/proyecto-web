from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class EmpresaBase(BaseModel):
    nombre: Optional[str]
    id_tipo_empresa: Optional[int]
    id_direccion: Optional[int] = None
    estado: Optional[bool] = True

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(EmpresaBase):
    pass

class EmpresaOut(EmpresaBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        orm_mode = True

class EmpresaList(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True

class EmpresaAcceso(EmpresaBase):
    id: int    
    nombre: str
    id_tipo_empresa: str
    id_direccion: Optional[int] = None    

    class Config:
        orm_mode = True       

class UsuarioListado(BaseModel):
    username: str
    nombre: str
    class Config:
        orm_mode = True           