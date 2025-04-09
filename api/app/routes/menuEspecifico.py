from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.models import MenuGeneral
from app.database import SessionLocal


router = APIRouter(tags=["Menu"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/" )
def getGenerales(db: Session = Depends(get_db)):
    return {"hola":"hola"}



# @router.get("/especificos/all", response_model=MenuGeneral)
# def getEspecificos(empresa: EmpresaCreate, db: Session = Depends(get_db)):
#     return crear_empresa(db, empresa)
