from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TemplateBase(BaseModel):
    name: str
    subject: str
    body_html: str

class TemplateCreate(TemplateBase):
    pass

class TemplateOut(TemplateBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
