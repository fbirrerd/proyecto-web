from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.comuna import ComunaCreate, ComunaUpdate
from app.schemas.respond import objRespuesta
from app.services.comuna import create, get_all, get_by_id, get_by_id_provincia, update
from app.database import SessionLocal

router = APIRouter(tags=["Comuna"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def create_comuna(comuna: ComunaCreate, db: Session = Depends(get_db)):
    try:
        datos = create(db, comuna)
        return objRespuesta(
            respuesta=True,
            data=datos
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear comuna: {str(e)}")

@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_comunas(db: Session = Depends(get_db)):
    try:
        datos = get_all(db)
        return objRespuesta(
            respuesta=True,
            data=datos
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener comunas: {str(e)}")

@router.get("/provincia/{id_provincia}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_comunas_by_provincia(id_provincia: int, db: Session = Depends(get_db)):
    try:
        datos = get_by_id_provincia(db, id_provincia)
        if datos is None:
            raise HTTPException(status_code=404, detail="No se encontraron comunas para esta provincia")
        return objRespuesta(
            respuesta=True,
            data=datos
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener comunas por provincia: {str(e)}")

@router.get("/{id_comuna}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_comuna(id_comuna: int, db: Session = Depends(get_db)):
    try:
        datos = get_by_id(db, id_comuna)
        if datos is None:
            raise HTTPException(status_code=404, detail="Comuna no encontrada")
        return objRespuesta(
            respuesta=True,
            data=datos
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener comuna: {str(e)}")

@router.put("/{comuna_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def update_comuna(comuna_id: int, obj: ComunaUpdate, db: Session = Depends(get_db)):
    try:
        datos = update(db, comuna_id, obj)
        if datos is None:
            raise HTTPException(status_code=404, detail="Comuna no encontrada para actualizar")
        return objRespuesta(
            respuesta=True,
            data=datos
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar comuna: {str(e)}")
