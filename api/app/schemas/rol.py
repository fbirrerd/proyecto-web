from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RolBase(BaseModel):
    nombre: str
    estado: bool = True

class RolCreate(RolBase):
    pass

class RolUpdate(RolBase):
    pass

class RolOut(RolBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        orm_mode = True


class RolAcceso(RolBase):
    id: int    
    nombre: str
    class Config:
        orm_mode = True
        
class RolList(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True        