from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class DireccionBase(BaseModel):
    calle: str
    numero: Optional[str] = None
    complemento: Optional[str] = None
    id_comuna: Optional[int] = None
    id_provincia: Optional[int] = None
    id_region: Optional[int] = None
    codigo_postal: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    estado: Optional[bool] = True

class DireccionCreate(DireccionBase):
    pass

class DireccionUpdate(DireccionBase):
    pass

class DireccionOut(DireccionBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        orm_mode = True
