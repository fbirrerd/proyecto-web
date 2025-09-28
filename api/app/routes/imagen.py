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
def read_imagenes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        data = get_imagenes(db, skip=skip, limit=limit)
        return objRespuesta(
            respuesta = True, 
            data = data
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al obtener registros: {str(e)}"
        )


@router.get("/{imagen_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_imagen(imagen_id: int, db: Session = Depends(get_db)):
    try:
        data = get_imagen(db, imagen_id=imagen_id)
        if datos is None:
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
        return objRespuesta(
            respuesta = True, 
            data = data
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al obtener registros: {str(e)}"
        )

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def crear_imagen(imagen: ImagenCreate, db: Session = Depends(get_db)):
    try:
        data = create_imagen(db, imagen)
        return objRespuesta(
            respuesta = True, 
            data = data
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al crear registro: {str(e)}"
        )


@router.put("/{imagen_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def actualizar_imagen(imagen_id: int, imagen: ImagenUpdate, db: Session = Depends(get_db)):
    try:
        data = update_imagen(db, imagen_id, imagen)
        if datos is None:
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
        return objRespuesta(
            respuesta = True, 
            data = data
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al crear registro: {str(e)}"
        )
        
        
    return db_imagen

@router.delete("/{imagen_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def eliminar_imagen(imagen_id: int, db: Session = Depends(get_db)):
    db_imagen = delete_imagen(db, imagen_id)
    if not db_imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return db_imagen
