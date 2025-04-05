from fastapi import FastAPI
from app.database import Base, engine
from app.routes import empresa, usuario, usuario_empresa

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API con FastAPI y PostgreSQL")

app.include_router(empresa.router)
app.include_router(usuario.router)
app.include_router(usuario_empresa.router)
