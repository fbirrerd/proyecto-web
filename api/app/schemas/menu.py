from pydantic import BaseModel


class MenuSchema(BaseModel):
    id: int
    nombre: str
    tipo: str
    url: str
    icono: str | None
    orden: int | None
    padre_id: int | None
    estado: int 

    class Config:
        orm_mode = True