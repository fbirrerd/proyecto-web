from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    userName: str
    email: str
    class Config:
        from_attributes = True
class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioOut(UsuarioBase):
    id: int
    fecha_creacion: datetime
    estado: int
    duracion: int
    class Config:
        from_attributes = True


# Modelos Pydantic (con descripciones)
class UsuarioLogin(BaseModel):
    userName: str = Field(None, description="Nombre de usuario para el login.", example="admin")
    password: str = Field(None, description="Contraseña del usuario.", example="supersecret")


class UsuarioCambioPassword(BaseModel):
    userName: str = Field(None, description="Nombre de usuario para el login.", example="admin")
    email: str = Field(None, description="Correo asociado al login.", example="admin@admin.com")
    password: str = Field(None, description="Nueva password que se desea ingresar.", example="nuevaPassword")
