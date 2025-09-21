
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
# ----------------------------
# Laboratorio
# ----------------------------
class LaboratorioBase(BaseModel):
    nombre_laboratorio: str = Field(..., max_length=100)
    pais: Optional[str] = None
    direccion: Optional[str] = None
    sitio_web: Optional[str] = None
    contacto: Optional[str] = None
    id_empresa: int
    estado: Optional[bool] = False

class LaboratorioCreate(LaboratorioBase):
    pass

class LaboratorioUpdate(BaseModel):
    nombre_laboratorio: Optional[str] = None
    pais: Optional[str] = None
    direccion: Optional[str] = None
    sitio_web: Optional[str] = None
    contacto: Optional[str] = None
    estado: Optional[bool] = None

class LaboratorioOut(LaboratorioBase):
    id_laboratorio: int
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None

    class Config:
        orm_mode = True

