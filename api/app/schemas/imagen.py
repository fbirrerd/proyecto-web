from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ImagenBase(BaseModel):
    url: str
    descripcion: Optional[str] = None
    id_medicamento: Optional[int] = None
    id_laboratorio: Optional[int] = None
    id_persona: Optional[int] = None
    estado: Optional[bool] = True

class ImagenCreate(ImagenBase):
    pass

class ImagenUpdate(ImagenBase):
    pass

class ImagenOut(ImagenBase):
    id_imagen: int
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        orm_mode = True
