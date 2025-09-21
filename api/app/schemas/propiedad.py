from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- Propiedades ---
class PropiedadBase(BaseModel):
    propiedad: str
    tipo: str   # texto, numero, opciones, select
    posibles_valores: Optional[str] = None

class PropiedadCreate(PropiedadBase):
    pass

class PropiedadUpdate(BaseModel):
    propiedad: Optional[str]
    tipo: Optional[str]
    posibles_valores: Optional[str]

class PropiedadOut(PropiedadBase):
    id: int
    class Config:
        orm_mode = True
