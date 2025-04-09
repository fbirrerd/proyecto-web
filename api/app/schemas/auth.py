from pydantic import BaseModel, Field


# Modelos Pydantic (con descripciones)
class UsuarioLogin(BaseModel):
    username: str = Field(None, description="Nombre de usuario para el login.", example="admin")
    password: str = Field(None, description="Contraseña del usuario.", example="supersecret")


class UsuarioCambioPassword(BaseModel):
    username: str = Field(None, description="Nombre de usuario para el login.", example="admin")
    email: str = Field(None, description="Correo asociado al login.", example="admin@admin.com")
    password: str = Field(None, description="Nueva password que se desea ingresar.", example="nuevaPassword")

class LoginReload(BaseModel):
    token: str = Field(None, description="token del usuario conectado", example="admin")
    empresaid: int = Field(None, description="Id de la empresa", example="supersecret")

