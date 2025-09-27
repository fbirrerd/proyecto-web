from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.imagen import ImagenCreate, ImagenUpdate
from app.schemas.respond import objRespuesta
from app.services.imagen import create_imagen, delete_imagen, get_imagen, get_imagenes, update_imagen
from app.database import SessionLocal, get_db

router = APIRouter(tags=["Imagen"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def listar_imagenes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_imagenes(db, skip=skip, limit=limit)

@router.get("/{imagen_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_imagen(imagen_id: int, db: Session = Depends(get_db)):
    db_imagen = get_imagen(db, imagen_id=imagen_id)
    if not db_imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return db_imagen

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def crear_imagen(imagen: ImagenCreate, db: Session = Depends(get_db)):
    return create_imagen(db, imagen)

@router.put("/{imagen_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def actualizar_imagen(imagen_id: int, imagen: ImagenUpdate, db: Session = Depends(get_db)):
    db_imagen = update_imagen(db, imagen_id, imagen)
    if not db_imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return db_imagen

@router.delete("/{imagen_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def eliminar_imagen(imagen_id: int, db: Session = Depends(get_db)):
    db_imagen = delete_imagen(db, imagen_id)
    if not db_imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return db_imagen
