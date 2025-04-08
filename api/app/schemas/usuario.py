# app/schemas/usuario.py
from pydantic import BaseModel, Field
from typing import Optional

class UsuarioBase(BaseModel):
    username: str
    nombres: str
    apellidos: str
    email: str
    direccion_id: Optional[int] = None
    duracion: Optional[int] = 20

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(UsuarioBase):
    password: Optional[str] = None

class UsuarioOut(UsuarioBase):
    id: int
    fecha_creacion: str
    fecha_modificacion: str
    estado: int

    class Config:
        orm_mode = True



# Modelos Pydantic (con descripciones)
class UsuarioLogin(BaseModel):
    userName: str = Field(None, description="Nombre de usuario para el login.", example="admin")
    password: str = Field(None, description="Contraseña del usuario.", example="supersecret")


class UsuarioCambioPassword(BaseModel):
    userName: str = Field(None, description="Nombre de usuario para el login.", example="admin")
    email: str = Field(None, description="Correo asociado al login.", example="admin@admin.com")
    password: str = Field(None, description="Nueva password que se desea ingresar.", example="nuevaPassword")
