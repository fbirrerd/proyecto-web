from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.respond import objRespuesta
from app.schemas.vademecum_medicamentos import MedicamentoCreate, MedicamentoOut, MedicamentoUpdate
from app.services.vademecum_medicamentos import create_medicamento, delete_medicamento, get_medicamento, list_medicamentos, update_medicamento
from app.database import get_db


router = APIRouter(tags=["VademecumMedicamento"])

# ---- Medicamentos ----
@router.post("/medicamentos", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def api_create_medicamento(payload: MedicamentoCreate, db: Session = Depends(get_db)):
    return create_medicamento(db, payload)

@router.get("/medicamentos", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def api_list_medicamentos(
    id_empresa: Optional[int] = Query(None),
    q: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(8, ge=1, le=100),
    db: Session = Depends(get_db)
):
    items, total = list_medicamentos(db, id_empresa, q, page, per_page)
    return items

@router.get("/medicamentos/{id_medicamento}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def api_get_medicamento(id_medicamento: int, db: Session = Depends(get_db)):
    obj = get_medicamento(db, id_medicamento)
    if not obj:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado")
    return obj

@router.put("/medicamentos/{id_medicamento}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def api_update_medicamento(id_medicamento: int, payload: MedicamentoUpdate, db: Session = Depends(get_db)):
    obj = update_medicamento(db, id_medicamento, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado")
    return obj

@router.delete("/medicamentos/{id_medicamento}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def api_delete_medicamento(id_medicamento: int, db: Session = Depends(get_db)):
    ok = delete_medicamento(db, id_medicamento)
    if not ok:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado")
    return {"ok": True}