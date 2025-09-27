from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DashboardInicialBase(BaseModel):
    pagina: str
    estado: Optional[bool] = True

class DashboardInicialCreate(DashboardInicialBase):
    pass

class DashboardInicialUpdate(BaseModel):
    pagina: Optional[str] = None
    estado: Optional[bool] = None

class DashboardInicialOut(DashboardInicialBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        orm_mode = True