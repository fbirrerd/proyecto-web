from datetime import datetime
from pydantic import BaseModel
from typing import Any, List, Optional

from app.schemas.usuario import AccesoUsuario
from app.schemas.menus import MenuAcceso
from app.schemas.rol import RolAcceso
from app.schemas.empresa import EmpresaAcceso


# Clase que representa la duración del acceso
class AccesoDuracion    (BaseModel):
    inicio: datetime
    termino: datetime
    minutos: int

    class Config:
        orm_mode = True

class AccesoPagina(BaseModel):
    inicio: Optional[str] = None
    dashboard: Optional[str] = None
    class Config:
        orm_mode = True 



# Clase que representa los datos de acceso del usuario
class DatosAcceso(BaseModel):
    username: str
    email: str
    token: str
    usuario: AccesoUsuario
    menus: Optional[List[MenuAcceso]] = None
    empresas: List[EmpresaAcceso]
    empresaSeleccionada: Optional[int] = None
    roles: Optional[List[RolAcceso]] = None
    modulos: Optional[List[Any]] = None
    duracionAcceso: AccesoDuracion
    pagina: Optional[AccesoPagina] = None
    class Config:
        orm_mode = True 
            
