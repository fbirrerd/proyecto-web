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

    class Config:
        orm_mode = True    

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

class UsuarioAcceso(UsuarioBase):
    id: int
    username: str
    nombres: str
    apellidos: str
    email: str
    direccion_id: Optional[int] = None
    class Config:
        orm_mode = True      

