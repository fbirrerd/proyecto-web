from fastapi import FastAPI
from app.database import Base, engine
from app.routes import empresa, usuario, usuario_empresa

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API con FastAPI y PostgreSQL")

app.include_router(empresa.router,prefix="/api/v1/empresa")
app.include_router(usuario.router,prefix="/api/v1/usuario")
app.include_router(usuario_empresa.router,prefix="/api/v1/usuario")
