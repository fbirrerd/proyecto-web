from datetime import datetime
from pydantic import BaseModel
from typing import Any, List, Optional

from app.schemas.menus import MenuAcceso
from app.schemas.rol import RolAcceso
from app.schemas.empresa import EmpresaAcceso
from app.schemas.usuario import UsuarioAcceso


# Clase que representa la duración del acceso
class AccesoDuracion(BaseModel):
    inicio: datetime
    termino: datetime
    minutos: int

    class Config:
        orm_mode = True


# Clase que representa los datos de acceso del usuario
class DatosAcceso(BaseModel):
    username: str
    email: str
    token: str
    usuario: UsuarioAcceso
    menus: Optional[List[MenuAcceso]] = None
    empresas: List[EmpresaAcceso]
    empresaSeleccionada: Optional[int] = None
    roles: Optional[List[RolAcceso]] = None
    modulos: Optional[List[Any]] = None
    duracionAcceso: AccesoDuracion

    class Config:
        orm_mode = True
