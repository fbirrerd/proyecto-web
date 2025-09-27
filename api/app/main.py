from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import imagen
from app.routes import vademecum_categoria, vademecum_laboratorio, vademecum_medicamento
from app.routes import propiedad, propiedad_empresa
from app.database import init_db
from app.config import ALLOWED_ORIGINS

# Importación de routers agrupados
from app.routes import (
    auth, empresa, usuario, menus, rol, rolMenu,
    empresaUsuarioRol, tipoEmpresa,
    tipoMenu, modulo, moduloMenu, empresaModulo,
    region, provincia, comuna, nacionalidad, vademecum
)

# Inicialización de la aplicación
app = FastAPI(
    title="Sistema de Gestión de Menús",
    description="API para gestionar menús, usuarios, roles y empresas.",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialización de la base de datos al iniciar la app
@app.on_event("startup")
def startup():
    init_db()
    print("✅ Base de datos inicializada correctamente.")

# Endpoints principales
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(empresa.router, prefix="/api/v1/empresa")
app.include_router(usuario.router, prefix="/api/v1/usuario")
app.include_router(menus.router, prefix="/api/v1/menu")
app.include_router(rol.router, prefix="/api/v1/rol")
app.include_router(modulo.router, prefix="/api/v1/modulo")


# Endpoints tablas tipos
app.include_router(tipoEmpresa.router, prefix="/api/v1/tipoempresa")
app.include_router(tipoMenu.router, prefix="/api/v1/tipomenu")


# Endpoints tablas relacionadas
app.include_router(moduloMenu.router, prefix="/api/v1/modulomenu")
app.include_router(empresaModulo.router, prefix="/api/v1/empresamodulo")
app.include_router(rolMenu.router, prefix="/api/v1/rolmenu")
app.include_router(empresaUsuarioRol.router, prefix="/api/v1/empresausuariorol")

# Endpoints geográficos
app.include_router(region.router, prefix="/api/v1/region")
app.include_router(provincia.router, prefix="/api/v1/provincia")
app.include_router(comuna.router, prefix="/api/v1/comuna")
app.include_router(nacionalidad.router, prefix="/api/v1/nacionalidad")


app.include_router(propiedad.router, prefix="/api/v1/propiedad")
app.include_router(propiedad_empresa.router, prefix="/api/v1/propiedad_empresa")

app.include_router(vademecum.router, prefix="/api/v1/vademecum")
app.include_router(vademecum_categoria.router, prefix="/api/v1/vademecum/categoria")
app.include_router(vademecum_laboratorio.router, prefix="/api/v1/vademecum/laboratorio")
app.include_router(vademecum_medicamento.router, prefix="/api/v1/vademecum/medicamento")


app.include_router(imagen.router, prefix="/api/v1/imagen")


# Ruta raíz
@app.get("/")
def read_root():
    return {"message": "🚀 API de gestión activa y funcionando correctamente."}
