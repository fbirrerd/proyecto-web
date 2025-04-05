from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.usuario_empresa import UsuarioEmpresaCreate, UsuarioEmpresaOut
from app.services.usuario_empresa import crear_usuario_empresa

router = APIRouter(prefix="/usuario-empresa", tags=["UsuarioEmpresa"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UsuarioEmpresaOut)
def crear(relacion: UsuarioEmpresaCreate, db: Session = Depends(get_db)):
    return crear_usuario_empresa(db, relacion)
