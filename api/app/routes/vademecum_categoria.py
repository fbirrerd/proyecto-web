from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.respond import objRespuesta
from app.schemas.vademecum_categoria import CategoriaCreate, CategoriaOut, CategoriaUpdate
from app.services.vademecum_categoria import create_categoria, delete_categoria, get_categoria, list_categorias, update_categoria
from app.database import get_db

router = APIRouter(tags=["VademecumCategoria"])

# ---- Categorias ----
@router.post("/categorias", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def api_create_categoria(payload: CategoriaCreate, db: Session = Depends(get_db)):
    return create_categoria(db, payload)

@router.get("/categorias", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def api_list_categorias(
    id_empresa: Optional[int] = Query(None),
    q: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    items, total = list_categorias(db, id_empresa, q, page, per_page)
    return items

@router.get("/categorias/{id_categoria}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def api_get_categoria(id_categoria: int, db: Session = Depends(get_db)):
    obj = get_categoria(db, id_categoria)
    if not obj:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return obj

@router.put("/categorias/{id_categoria}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def api_update_categoria(id_categoria: int, payload: CategoriaUpdate, db: Session = Depends(get_db)):
    obj = update_categoria(db, id_categoria, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return obj

@router.delete("/categorias/{id_categoria}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def api_delete_categoria(id_categoria: int, db: Session = Depends(get_db)):
    ok = delete_categoria(db, id_categoria)
    if not ok:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return {"ok": True}