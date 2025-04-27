from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Esquema base para la clase EmpresaUsuarioRol
class EmpresaUsuarioRolBase(BaseModel):
    id_empresa: int
    id_usuario: int
    id_rol: int
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None
    estado: bool

    class Config:
        orm_mode = True

# Esquema de salida para la respuesta al obtener un "EmpresaUsuarioRol"
class EmpresaUsuarioRolOut(EmpresaUsuarioRolBase):
    pass

# Esquema para la entrada al crear un "EmpresaUsuarioRol"
class EmpresaUsuarioRolCreate(EmpresaUsuarioRolBase):
    pass

# Esquema para la entrada al actualizar un "EmpresaUsuarioRol" (actualización parcial)
class EmpresaUsuarioRolUpdate(BaseModel):
    fecha_modificacion: Optional[datetime] = None
    estado: Optional[bool] = None
        
class EmpresaUsuarioRolList(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True              