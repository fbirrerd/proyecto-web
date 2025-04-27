from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EmailBase(BaseModel):
    to_address: EmailStr
    cc_address: Optional[str] = None
    bcc_address: Optional[str] = None
    subject: str
    body_html: str
    template_id: Optional[int] = None

class EmailCreate(EmailBase):
    pass

class EmailOut(EmailBase):
    id: int
    status: str
    created_at: datetime
    sent_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        
class EmailIn(BaseModel):
    from_address: str
    to_address: str
    cc_address: Optional[str] = None
    bcc_address: Optional[str] = None
    subject: str
    parameters: Optional[str] = None
    template: Optional[str] = None

    class Config:
        orm_mode = True
        
