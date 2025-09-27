from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.respond import objRespuesta
from app.schemas.vademecum_laboratorio import LaboratorioCreate, LaboratorioOut, LaboratorioUpdate
from app.services.vademecum_laboratorio import create_laboratorio, delete_laboratorio, get_laboratorio, list_laboratorios, update_laboratorio
from app.database import get_db


router = APIRouter(tags=["VademecumLaboratorio"])

# ---- Laboratorios ----
@router.post("/laboratorios", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def api_create_laboratorio(payload: LaboratorioCreate, db: Session = Depends(get_db)):
    return create_laboratorio(db, payload)

@router.get("/laboratorios", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def api_list_laboratorios(
    id_empresa: Optional[int] = Query(None),
    q: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    items, total = list_laboratorios(db, id_empresa, q, page, per_page)
    # opcional: devolver metadata en headers o estructura
    return items

@router.get("/laboratorios/{id_laboratorio}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def api_get_laboratorio(id_laboratorio: int, db: Session = Depends(get_db)):
    obj = get_laboratorio(db, id_laboratorio)
    if not obj:
        raise HTTPException(status_code=404, detail="Laboratorio no encontrado")
    return obj

@router.put("/laboratorios/{id_laboratorio}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def api_update_laboratorio(id_laboratorio: int, payload: LaboratorioUpdate, db: Session = Depends(get_db)):
    obj = update_laboratorio(db, id_laboratorio, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Laboratorio no encontrado")
    return obj

@router.delete("/laboratorios/{id_laboratorio}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def api_delete_laboratorio(id_laboratorio: int, db: Session = Depends(get_db)):
    ok = delete_laboratorio(db, id_laboratorio)
    if not ok:
        raise HTTPException(status_code=404, detail="Laboratorio no encontrado")
    return {"ok": True}
