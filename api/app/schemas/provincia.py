from pydantic import BaseModel

class ProvinciaBase(BaseModel):
    nombre: str
    codigo: str
    id_region: int
    estado: bool = True

class ProvinciaCreate(ProvinciaBase):
    pass

class Provincia(ProvinciaBase):
    id: int

    class Config:
        orm_mode = True

class ProvinciaUpdate(ProvinciaBase):
    id: int

    class Config:
        orm_mode = True
