from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    userName: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioOut(UsuarioBase):
    id: int
    fecha_creacion: datetime
    estado: int
    duracion: int

    class Config:
        from_attributes = True

class UsuarioLogin(UsuarioBase):
    userName: str
    password: str

class UsuarioCambioPassword(UsuarioBase):
    userName: str
    correo: str
    password: str

class UsuarioLoginRespuesta(UsuarioBase):
    respuesta: bool
    resultado: object
    cambioClave: Optional[bool] = None
    error: Optional[str] = None
