from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.propiedad_empresa import PropiedadEmpresaCreate, PropiedadEmpresaUpdate
from app.schemas.respond import objRespuesta
from app.database import SessionLocal, get_db



router = APIRouter(tags=["PropiedadEmpresa"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# --- Propiedades Empresa ---
@router.post("/empresa", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def create_propiedad_empresa(payload: PropiedadEmpresaCreate, db: Session = Depends(get_db)):
    return create_propiedad_empresa(db, payload)

@router.get("/empresa", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def list_propiedades_empresa(empresa_id: Optional[int] = None, db: Session = Depends(get_db)):
    return list_propiedades_empresa(db, empresa_id)

@router.get("/empresa/{id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def get_propiedad_empresa(id: int, db: Session = Depends(get_db)):
    obj = get_propiedad_empresa(db, id)
    if not obj:
        raise HTTPException(404, "PropiedadEmpresa no encontrada")
    return obj

@router.put("/empresa/{id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def update_propiedad_empresa(id: int, payload: PropiedadEmpresaUpdate, db: Session = Depends(get_db)):
    obj = update_propiedad_empresa(db, id, payload)
    if not obj:
        raise HTTPException(404, "PropiedadEmpresa no encontrada")
    return obj

@router.delete("/empresa/{id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def delete_propiedad_empresa(id: int, db: Session = Depends(get_db)):
    ok = delete_propiedad_empresa(db, id)
    if not ok:
        raise HTTPException(404, "PropiedadEmpresa no encontrada")
    return {"ok": True}