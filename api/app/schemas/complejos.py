from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

# Clase que representa los datos de acceso del usuario
class DatosAcceso(BaseModel):
    nombre_usuario: str
    email: str
    token: str
    empresas: Optional[List['AccesoEmpresas']]  # Lista de empresas, usamos Forward Reference
    empresaSeleccionada: int
    # roles: List['AccesoRoles']
    # menu: List['AccesoMenu']

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
    id: int
    nombre: str
    url: str

    class Config:
        orm_mode = True


# Actualizar las referencias para resolver Forward References
DatosAcceso.update_forward_refs()
