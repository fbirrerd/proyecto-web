# app/schemas/usuario.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class UsuarioBase(BaseModel):
    username: str
    email: str
    duracion: Optional[int] = 20
    pagina_inicio: Optional[str] = "/"
    id_dashboard: Optional[int] = None
    id_persona: Optional[int] = None
    estado: Optional[bool] = True


class UsuarioCreate(UsuarioBase):
    password: str  # requerido al crear usuario


class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    duracion: Optional[int] = None
    pagina_inicio: Optional[str] = None
    id_dashboard: Optional[int] = None
    id_persona: Optional[int] = None
    estado: Optional[bool] = None


class UsuarioOut(UsuarioBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        orm_mode = True
        
class AccesoUsuario(BaseModel):
    id: int
    username: str
    email: str
    duracion: Optional[int] = 20
    id_dashboard: Optional[int]
    id_persona: Optional[int]
    id_direccion: Optional[int] = None
    estado: Optional[bool] = True
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

     
           
        