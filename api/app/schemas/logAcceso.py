from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LogAccesoBase(BaseModel):
    username: str
    exito: bool
    mensaje: str
    ip: Optional[str] = None
    user_agent: Optional[str] = None
    id_usuario: Optional[int] = None

class LogAccesoCreate(LogAccesoBase):
    pass

class LogAccesoOut(LogAccesoBase):
    id: int
    fecha: datetime

    class Config:
        orm_mode = True
