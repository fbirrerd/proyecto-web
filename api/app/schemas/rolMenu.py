from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class RolMenuBase(BaseModel):
    id: int
    nombre: str


class RolMenu(RolMenuBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        orm_mode = True

class RelacionMenuRol(BaseModel):
    id_menu: int
    id_rol: int
    estado: bool
    class Config:
        orm_mode = True
        
class ObjetoRelaciones(BaseModel):
    relaciones: List[RelacionMenuRol]
    class Config:
        orm_mode = True
        
class RolMenu_relacion(RolMenuBase):

    class Config:
        orm_mode = True        