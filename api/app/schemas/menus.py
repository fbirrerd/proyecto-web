from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class MenuBase(BaseModel):
    nombre: Optional[str] = None
    icono: Optional[str] = None
    url: Optional[str] = None
    id_padre: Optional[int] = None
    es_publico: Optional[bool] = False
    estado: Optional[bool] = True
    class Config:
        orm_mode = True  # Esto permite que Pydantic utilice objetos SQLAlchemy

class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    id: int
    nombre: str
    icono: str
    url: Optional[str] = None    
    tipo: Optional[str] = None
    id_padre: Optional[int] = None

class MenuEstadoUpdate(BaseModel):
    id: int
    estado: bool

class MenuOut(MenuBase):
    id: int
    id_padre: Optional[int] = None
    hijos: Optional[bool] 
    nivel: Optional[bool] = 0
    class Config:
        orm_mode = True

class MenuAcceso(MenuBase):
    id: Optional[int] = None
    tipo: Optional[str] = None
    orden: Optional[int] = None 
    url: Optional[str] = None

  
    class Config:
        orm_mode = True
        
class MenuInput(BaseModel):
    nombre: str
    icono: str
    id_tipo_menu: int
    id_padre: Optional[int]
    url: str
    descripcion: Optional[str]
    orden: Optional[int]
    estado: bool
    roles: List[int]  # ← esto es nuevo        
        
