from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

# Clase que representa los datos de acceso del usuario
class DatosAcceso(BaseModel):
    nombre_usuario: str
    email: EmailStr
    token: str
    duracionAcceso: 'AccesoDuracion'  # Usamos 'string' para el tipo anticipado de la clase
    empresas: List['AccesoEmpresas']  # Lista de empresas
    empresaSeleccionada: int

# Clase que representa la duración del acceso
class AccesoDuracion(BaseModel):
    inicio: datetime
    termino: datetime
    minutos: int

# Clase que representa la información de la empresa
class AccesoEmpresas(BaseModel):
    id: int
    rut: str
    nombre: str
