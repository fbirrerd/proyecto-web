from pydantic import BaseModel

class NacionalidadBase(BaseModel):
    nombre: str
    codigo: str
    estado: bool = True

class NacionalidadCreate(NacionalidadBase):
    pass

class Nacionalidad(NacionalidadBase):
    id: int

    class Config:
        orm_mode = True


class NacionalidadUpdate(NacionalidadBase):
    id: int

    class Config:
        orm_mode = True