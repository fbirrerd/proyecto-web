from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class HTTPRespuesta(BaseModel):
    respuesta: bool
    error: Optional[str] = None


