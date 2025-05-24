from pydantic import BaseModel

class RegionBase(BaseModel):
    nombre: str
    codigo: str
    estado: bool = True

class RegionCreate(RegionBase):
    pass

class Region(RegionBase):
    id: int

    class Config:
        orm_mode = True

class RegionUpdate(RegionBase):
    id: int

    class Config:
        orm_mode = True
