
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
# ----------------------------
# Categoria Terapeutica
# ----------------------------
class CategoriaBase(BaseModel):
    nombre_categoria: str = Field(..., max_length=100)
    descripcion: Optional[str] = None
    id_empresa: int
    estado: Optional[bool] = False

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre_categoria: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[bool] = None

class CategoriaOut(CategoriaBase):
    id_categoria: int
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None

    class Config:
        orm_mode = True

