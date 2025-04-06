from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import empresa, usuario, usuario_empresa

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API con FastAPI y PostgreSQL")
# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes (puedes restringirlo a ['http://localhost:3000'])
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

app.include_router(empresa.router,prefix="/api/v1/empresa")
app.include_router(usuario.router,prefix="/api/v1/usuario")
app.include_router(usuario_empresa.router,prefix="/api/v1/usuario")
