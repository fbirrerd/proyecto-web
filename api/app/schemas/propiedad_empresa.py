from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.propiedad import PropiedadOut

class PropiedadEmpresaBase(BaseModel):
    empresa_id: int
    propiedad_id: int
    valor: str

class PropiedadEmpresaCreate(PropiedadEmpresaBase):
    pass

class PropiedadEmpresaUpdate(BaseModel):
    valor: Optional[str]

class PropiedadEmpresaOut(PropiedadEmpresaBase):
    id: int
    propiedad: Optional[PropiedadOut]
    class Config:
        orm_mode = True