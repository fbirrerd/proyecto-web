from pydantic import BaseModel
from typing import Any, Optional, List
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

class ModuloNombre(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        orm_mode = True

class ModuloConArbol(BaseModel):
    id: int
    nombre: str
    descripcion: str
    arbol: Optional[list[Any]]

    class Config:
        orm_mode = True
        
        
class ModuloPermiso(BaseModel):
    id: int
    nombre: str
    descripcion: str
    check: bool        
    
class ModuloRelacionCreate(BaseModel):
    id_modulo: int
    estado: bool
