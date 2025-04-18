from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes import auth, empresa, menus, usuario, rol, rolMenu
from app.config import ALLOWED_ORIGINS

# Inicializar base de datos
init_db()

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

# Endpoints agrupados por contexto
app.include_router(auth.router,     prefix="/api/v1/auth")
app.include_router(empresa.router,  prefix="/api/v1/empresa")
app.include_router(usuario.router,  prefix="/api/v1/usuario")
app.include_router(menus.router,    prefix="/api/v1/menu") 
app.include_router(rol.router,      prefix="/api/v1/rol")
app.include_router(rolMenu.router,  prefix="/api/v1/rolmenu")
# app.include_router(menuEspecifico.router, prefix="/api/v1/menue")  # Activar si se usa

@app.get("/")
def read_root():
    return {"message": "API de gestión activa 🚀"}
