
from fastapi import FastAPI
from routes import email, template  # Asegúrate de que este import esté bien

app = FastAPI(
    title="Sistema de Correos",
    description="API para gestionar correos electrónicos.",
    version="1.0.0"
)

# Incluir el router de emails
app.include_router(email.router, prefix="/api/v1")
app.include_router(template.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "API de gestión activa 🚀"}

