from typing import Optional
from pydantic import BaseModel, Field


class objRespuesta(BaseModel):
    respuesta: Optional[bool] = Field(None, description="Indica si la operación fue exitosa", example=True)
    data: Optional[object] = Field(None, description="Objeto con los datos de respuesta")

    # Método que excluye campos con valores None
    def dict_without_none(self):
        return self.model_dump(exclude_none=True)
