from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MenuGeneralBase(BaseModel):
    nombre: Optional[str] = None
    icono: Optional[str] = None
    ruta: Optional[str] = None
    id_padre: Optional[int] = None
    es_publico: Optional[bool] = False
    estado: Optional[bool] = True
    class Config:
        orm_mode = True  # Esto permite que Pydantic utilice objetos SQLAlchemy

class MenuCreate(MenuGeneralBase):
    pass


class MenuUpdate(BaseModel):
    id: int
    nombre: str
    icono: str
    ruta: str
    tipo: str
    id_padre: Optional[int] = None

class MenuEstadoUpdate(BaseModel):
    id: int
    estado: bool

class MenuOut(MenuGeneralBase):
    id: int
    id_padre: Optional[int] = None
    hijos: Optional[bool] 
    nivel: Optional[bool] = 0
    class Config:
        orm_mode = True

class MenuGeneralAcceso(MenuGeneralBase):
    id: Optional[int] = None
    tipo: Optional[str] = None
    orden: Optional[int] = None 

  
    class Config:
        orm_mode = True
        
