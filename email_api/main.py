from fastapi import FastAPI
from email_api.routes import email  # Asegúrate de que este import esté bien

app = FastAPI(
    title="Sistema de Correos",
    description="API para gestionar correos electrónicos.",
    version="1.0.0"
)

# Incluir el router de emails
app.include_router(email.router, prefix="/api/v1/emails")

@app.get("/")
def read_root():
    return {"message": "API de gestión activa 🚀"}

