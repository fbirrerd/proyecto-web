from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Esquema para la clase EmpresaUsuario
class EmpresaUsuarioBase(BaseModel):
    id_empresa: int
    id_usuario: int
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None
    estado: bool

    class Config:
        orm_mode = True

# Esquema para la respuesta al obtener un "EmpresaUsuario"
class EmpresaUsuarioOut(EmpresaUsuarioBase):
    pass

# Esquema para la entrada al crear o actualizar un "EmpresaUsuario"
class EmpresaUsuarioCreate(EmpresaUsuarioBase):
    pass

# Esquema para la entrada al actualizar un "EmpresaUsuario" (se puede hacer parcialmente)
class EmpresaUsuarioUpdate(BaseModel):
    fecha_modificacion: Optional[datetime] = None
    estado: Optional[bool] = None
        
class EmpresaUsuarioList(BaseModel):
    usuario_id: int
    usuario_nombre: str
    empresa_id: int
    empresa_nombre: str
    estado: bool

    class Config:
        orm_mode = True              