from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    userName: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioOut(UsuarioBase):
    id: int
    fecha_creacion: datetime
    estado: int
    duracion: int

    class Config:
        from_attributes = True
# --- Asume que tienes estas dependencias y modelos definidos ---
# from your_app.database import get_db # Tu función para obtener Session
# from your_app.auth import validar_login_usuario # Tu lógica de validación
# ---

# Modelos Pydantic (con descripciones)
class UsuarioLogin(BaseModel):
    userName: str = Field(None, description="Nombre de usuario para el login.", example="admin")
    password: str = Field(None, description="Contraseña del usuario.", example="supersecret")


class UsuarioCambioPassword(BaseModel):
    userName: str = Field(None, description="Nombre de usuario para el login.", example="admin")
    correo: str = Field(None, description="Correo asociado al login.", example="admin@admin.com")
    nuevaPassword: str = Field(None, description="Nueva password que se desea ingresar.", example="nuevaPassword")

class UsuarioLoginRespuesta(BaseModel):
    respuesta: bool = Field(None, description="Retorna un boolean", example="true")
    data: Optional[object] = Field(None, description="Retorna el objeto con los datos")
    error: Optional[str] = Field(None, description="Retorna posibles errores", example="admin")

    # Método que excluye campos con valores None
    def dict_without_none(self):
    #    return self.model_dump_json(exclude_none=True)
        return self.model_dump_json(exclude_none=True)
