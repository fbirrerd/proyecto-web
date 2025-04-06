from datetime import datetime
from pydantic import BaseModel
from typing import List

# Clase que representa los datos de acceso del usuario
class DatosAcceso(BaseModel):
    nombre_usuario: str
    email: str
    token: str
    # duracionAcceso: 'AccesoDuracion'  # Usamos 'string' para el tipo anticipado de la clase
    # empresas: List['AccesoEmpresas']  # Lista de empresas
    # empresaSeleccionada: int
    # roles: List['AccesoRoles']
    # menu: List['AccesoMenu']
    class Config:
        # Esto permitirá que las referencias se resuelvan correctamente
        json_encoders = {
            # Puedes definir encoders si es necesario
        }


# Clase que representa la duración del acceso
class AccesoDuracion(BaseModel):
    inicio: datetime
    termino: datetime
    minutos: int
    class Config:
        # Esto permitirá que las referencias se resuelvan correctamente
        json_encoders = {
            # Puedes definir encoders si es necesario
        }

# Clase que representa la información de la empresa
class AccesoEmpresas(BaseModel):
    id: int
    nombre: str
    class Config:
        # Esto permitirá que las referencias se resuelvan correctamente
        json_encoders = {
            # Puedes definir encoders si es necesario
        }

# Clase que representa la información del rol
class AccesoRoles(BaseModel):
    id: int
    nombre: str
    class Config:
        # Esto permitirá que las referencias se resuelvan correctamente
        json_encoders = {
            # Puedes definir encoders si es necesario
        }

# Clase que representa el menú de acceso
class AccesoMenu(BaseModel):
    id: int
    nombre: str
    url: str
    class Config:
        # Esto permitirá que las referencias se resuelvan correctamente
        json_encoders = {
            # Puedes definir encoders si es necesario
        }


