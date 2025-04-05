from pydantic import BaseModel
from datetime import date

class UsuarioEmpresaBase(BaseModel):
    usuario_id: int
    empresa_id: int
    fecha_inicio: date
    fecha_fin: date | None = None

class UsuarioEmpresaCreate(UsuarioEmpresaBase):
    pass

class UsuarioEmpresaOut(UsuarioEmpresaBase):
    class Config:
        from_attributes = True
