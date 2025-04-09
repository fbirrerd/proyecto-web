from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.respond import objRespuesta
from app.schemas.menugeneral import MenuGeneralAcceso
from app.services.menuGenerales import getListMenuGenerales
from app.database import SessionLocal


router = APIRouter(tags=["Menu"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/generales/all", response_model=objRespuesta)
def getGenerales(db: Session = Depends(get_db)):
    return getListMenuGenerales(db)

# @router.get("/especificos/all", response_model=MenuGeneral)
# def getEspecificos(empresa: EmpresaCreate, db: Session = Depends(get_db)):
#     return crear_empresa(db, empresa)
