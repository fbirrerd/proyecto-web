from datetime import datetime
from pydantic import BaseModel
from typing import Any, List, Optional

from app.schemas.menus import MenuAcceso
from app.schemas.rol import RolAcceso
from app.schemas.empresa import EmpresaAcceso
from app.schemas.usuario import UsuarioAcceso


# Clase que representa los datos de acceso del usuario
class DatosAcceso(BaseModel):
    username: str
    email: str
    token: str
    usuario: UsuarioAcceso
    menus: Optional[List['MenuAcceso']]
    empresas: List['EmpresaAcceso']
    empresaSeleccionada: Optional[int] 
    roles: Optional[List['RolAcceso']] 
    modulos: Optional[List[Any]] 
    # duracionAcceso: AccesoDuracion


    class Config:
        orm_mode = True


# Clase que representa la duración del acceso
class AccesoDuracion(BaseModel):
    inicio: datetime
    termino: datetime
    minutos: int

    class Config:
        orm_mode = True


# Clase que representa la información de la empresa
class AccesoEmpresas(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True


# Clase que representa la información del rol
class AccesoRoles(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True


# Clase que representa el menú de acceso
class AccesoMenu(BaseModel):
    nombre: str
    url: str

    class Config:
        orm_mode = True


# Actualizar las referencias para resolver Forward References
DatosAcceso.update_forward_refs()
