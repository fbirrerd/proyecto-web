
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ----------------------------
# Medicamento
# ----------------------------
class MedicamentoBase(BaseModel):
    nombre_comercial: str = Field(..., max_length=100)
    nombre_generico: str = Field(..., max_length=100)
    forma_farmaceutica: Optional[str] = None
    concentracion: Optional[str] = None
    id_laboratorio: int
    registro_sanitario: Optional[str] = None
    clasificacion: Optional[str] = None
    id_empresa: int
    estado: Optional[bool] = False

class MedicamentoCreate(MedicamentoBase):
    pass

class MedicamentoUpdate(BaseModel):
    nombre_comercial: Optional[str] = None
    nombre_generico: Optional[str] = None
    forma_farmaceutica: Optional[str] = None
    concentracion: Optional[str] = None
    id_laboratorio: Optional[int] = None
    registro_sanitario: Optional[str] = None
    clasificacion: Optional[str] = None
    estado: Optional[bool] = None

class MedicamentoOut(MedicamentoBase):
    id_medicamento: int
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None

    class Config:
        orm_mode = True
