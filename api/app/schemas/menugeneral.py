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


class MenuUpdate(MenuGeneralBase):
    id: int
    tipo: str
    orden: int


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
        
