from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.empresa import EmpresaCreate, EmpresaOut
from app.services.empresa import crear_empresa

router = APIRouter(tags=["Empresa"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=EmpresaOut)
def crear(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    return crear_empresa(db, empresa)
