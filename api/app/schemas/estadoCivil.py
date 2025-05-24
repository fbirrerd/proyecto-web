from pydantic import BaseModel

class EstadoCivilBase(BaseModel):
    nombre: str
    codigo: str
    estado: bool = True

class EstadoCivilCreate(EstadoCivilBase):
    pass

class EstadoCivil(EstadoCivilBase):
    id: int

    class Config:
        orm_mode = True

class EstadoCivilUpdate(EstadoCivilBase):
    id: int

    class Config:
        orm_mode = True
