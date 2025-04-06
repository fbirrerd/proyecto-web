from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ApiRespuesta(BaseModel):
    respuesta: bool = Field(None, description="Retorna un boolean", example="true")
    data: Optional[object] = Field(None, description="Retorna el objeto con los datos")
    error: Optional[str] = Field(None, description="Retorna texto de un posible error", example="admin")
    status_code: Optional[int] = Field(None, description="Retorna numero de un posible error", example=401)

    # Método que excluye campos con valores None
    def dict_without_none(self):
    #    return self.model_dump_json(exclude_none=True)
        return self.model_dump_json(exclude_none=True)
