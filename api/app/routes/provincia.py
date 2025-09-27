from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.provincia import ProvinciaCreate, ProvinciaUpdate
from app.schemas.respond import objRespuesta
from app.services.provincia import create, get_all, get_by_id, update
from app.database import SessionLocal

router = APIRouter(tags=["Provincia"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_provincias(db: Session = Depends(get_db)):
    try:
        datos = get_all(db)
        return objRespuesta(
            respuesta=True,
            data=datos
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener provincias: {str(e)}")

@router.get("/{id_provincia}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_provincia(id_provincia: int, db: Session = Depends(get_db)):
    try:
        db_provincia = get_by_id(db, id_provincia)
        if db_provincia is None:
            raise HTTPException(status_code=404, detail="Provincia no encontrada")
        return objRespuesta(
            respuesta=True,
            data=db_provincia
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener provincia: {str(e)}")

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def create_provincia(provincia: ProvinciaCreate, db: Session = Depends(get_db)):
    try:
        datos = create(db, provincia)
        return objRespuesta(
            respuesta=True,
            data=datos
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear provincia: {str(e)}")


@router.put("/{id_provincia}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def update_provincia(id_provincia: int, obj: ProvinciaUpdate, db: Session = Depends(get_db)):
    try:
        db_provincia = update(db, id_provincia, obj)
        if db_provincia is None:
            raise HTTPException(status_code=404, detail="Provincia no encontrada para actualizar")
        return objRespuesta(
            respuesta=True,
            data=db_provincia
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar provincia: {str(e)}")
