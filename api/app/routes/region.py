from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.region import RegionCreate, RegionUpdate
from app.schemas.respond import objRespuesta
from app.services.region import create, get_all, get_by_id, update
from app.database import SessionLocal

router = APIRouter(tags=["Region"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_regions(db: Session = Depends(get_db)):
    try:
        data = get_all(db)
        return objRespuesta(
            respuesta = True,
            data = data
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al obtener los registros: {str(e)}"
        )

@router.get("/{region_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_region(region_id: int, db: Session = Depends(get_db)):
    try:
        db_region = get_by_id(db, region_id)
        if db_region is None:
            raise HTTPException(status_code=404, detail="Región no encontrada")
        return objRespuesta(
            respuesta = True,
            data=db_region
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al obtener el registro: {str(e)}"
        )

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def create_region(region: RegionCreate, db: Session = Depends(get_db)):
    try:
        data = create(db, region)
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


@router.put("/{region_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def update_region(region_id: int, obj: RegionUpdate, db: Session = Depends(get_db)):
    try:
        db_region = update(db, region_id, obj)
        if db_region is None:
            raise HTTPException(status_code=404, detail="Región no encontrada para actualizar")
        return objRespuesta(
            respuesta = True,
            data=db_region
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al actualizar registro: {str(e)}"
        )
