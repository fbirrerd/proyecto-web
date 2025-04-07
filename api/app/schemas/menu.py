from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class TipoMenu(str, Enum):
    url = "url"
    formulario = "formulario"
    otro = "otro"

class MenuBase(BaseModel):
    id: int
    nombre: str
    tipo: TipoMenu
    valor: str
    icono: Optional[str]
    orden: Optional[int]
    padre_id: Optional[int]
    estado: int

class MenuTree(MenuBase):
    hijos: List["MenuTree"] = []

    class Config:
        orm_mode = True
