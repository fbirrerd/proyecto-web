# app/schemas/usuario.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class UsuarioBase(BaseModel):
    username: str
    nombre_mostrar: str

    email: str
    duracion: Optional[int] = 20
    estado: Optional[bool] = True
    class Config:
        orm_mode = True

class UsuarioCreate(UsuarioBase):
    password: Optional[str]
    id_direccion: Optional[int] = None

class UsuarioUpdate(BaseModel):
    nombre_mostrar: Optional[str]
    email: Optional[str]
    duracion: Optional[int]
    estado: Optional[bool]

class UsuarioOut(UsuarioBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        orm_mode = True

class UsuarioAcceso(UsuarioBase):
    id: int
    username: str
    nombre_mostrar: str
    email: str
    id_direccion: Optional[int] = None
    class Config:
        orm_mode = True      

class UsuarioList(BaseModel):
    id: int
    nombreCompleto: str
    class Config:
        orm_mode = True        
        
class UsuariosListado(BaseModel):
    id: int
    username: str
    nombre_mostrar: str
    email: str
    estado: Optional[bool] = True
    class Config:
        orm_mode = True     
        
class UsuarioId(BaseModel):
    id: int
    class Config:
        orm_mode = True     

class UsuarioCambioClave(BaseModel):
    id: int
    password: str 
    class Config:
        orm_mode = True     

class UsuarioCambioEstado(BaseModel):
    id: int 
    estado: str
    class Config:
        orm_mode = True     
           
        