from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.propiedad import PropiedadCreate, PropiedadUpdate
from app.schemas.respond import objRespuesta
from app.database import SessionLocal, get_db

router = APIRouter(tags=["Propiedad"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# --- Propiedades ---
@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def create_propiedad(payload: PropiedadCreate, db: Session = Depends(get_db)):
    try:
        return create_propiedad(db, payload)
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al crear registro: {str(e)}"
        )
    try:
        data = get_all(db=db)
        return objRespuesta(
            respuesta = True, 
            data=usuarios
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al obtener registros: {str(e)}"
        )
        

@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_propiedades(db: Session = Depends(get_db)):
    return list_propiedades(db)
    try:
        data = get_all(db=db)
        return objRespuesta(
            respuesta = True, 
            data=usuarios
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al obtener registros: {str(e)}"
        )

@router.get("/{id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def get_propiedad(id: int, db: Session = Depends(get_db)):
    obj = get_propiedad(db, id)
    if not obj:
        raise HTTPException(404, "Propiedad no encontrada")
    return obj

@router.put("/{id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def update_propiedad(id: int, payload: PropiedadUpdate, db: Session = Depends(get_db)):
    obj = update_propiedad(db, id, payload)
    if not obj:
        raise HTTPException(404, "Propiedad no encontrada")
    return obj

@router.delete("/{id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def delete_propiedad(id: int, db: Session = Depends(get_db)):
    ok = delete_propiedad(db, id)
    if not ok:
        raise HTTPException(404, "Propiedad no encontrada")
    return {"ok": True}
