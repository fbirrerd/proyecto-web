from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmailBase(BaseModel):
    de: str
    para: str
    conCopia: Optional[str] = None
    conCopiaOculta: Optional[str] = None
    asunto: Optional[str] = None
    parametros: str
    cuerpoHtml: Optional[str] = None

class EmailCreate(EmailBase):
    pass

class Email(EmailBase):
    id: int
    status: Optional[str] = "pending"
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
