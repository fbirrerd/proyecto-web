from pydantic import BaseModel

class ComunaBase(BaseModel):
    nombre: str
    codigo: str
    id_provincia: int
    estado: bool = True

class ComunaCreate(ComunaBase):
    pass

class Comuna(ComunaBase):
    id: int

    class Config:
        orm_mode = True

class ComunaUpdate(ComunaBase):
    id: int

    class Config:
        orm_mode = True
