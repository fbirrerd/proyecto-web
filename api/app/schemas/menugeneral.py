from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MenuBase(BaseModel):
    nombre: str
    icono: Optional[str] = None
    ruta: Optional[str] = None
    id_padre: Optional[int] = None
    es_publico: Optional[bool] = False
    estado: Optional[bool] = True


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class MenuOut(MenuBase):
    id: int
    fecha_creacion: Optional[datetime]
    fecha_modificacion: Optional[datetime]

    class Config:
        orm_mode = True

class MenuGeneralAcceso(MenuBase):
    id: int
    tipo: str    
    orden: int    
 
    class Config:
        orm_mode = True