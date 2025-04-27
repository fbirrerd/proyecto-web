from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TipoMenuBase(BaseModel):
    nombre: Optional[str]
    estado: Optional[bool] = True

class TipoMenuCreate(TipoMenuBase):
    pass

class TipoMenuUpdate(TipoMenuBase):
    pass

class TipoMenuOut(TipoMenuBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        orm_mode = True

class TipoMenuList(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True
        
class TipoMenuFiltro(BaseModel):
    id_tipo_empresa: int


    class Config:
        orm_mode = True        
        
class MenusOut(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True                