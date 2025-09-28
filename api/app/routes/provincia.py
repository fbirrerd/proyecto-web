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
        data = get_all(db)
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


@router.get("/{id_provincia}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_provincia(id_provincia: int, db: Session = Depends(get_db)):
    try:
        data = get_by_id(db, id_provincia)
        if data is None:
            raise HTTPException(status_code=404, detail="Provincia no encontrada")
        return objRespuesta(
            respuesta = True,
            data=data
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al obtener registros: {str(e)}"
        )

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def create_provincia(provincia: ProvinciaCreate, db: Session = Depends(get_db)):
    try:
        data = create(db, provincia)
        return objRespuesta(
            respuesta = True,
            data = data
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al crear registros: {str(e)}"
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al crear registros: {str(e)}"
        )


@router.put("/{id_provincia}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def update_provincia(id_provincia: int, obj: ProvinciaUpdate, db: Session = Depends(get_db)):
    try:
        db_provincia = update(db, id_provincia, obj)
        if db_provincia is None:
            raise HTTPException(status_code=404, detail="Provincia no encontrada para actualizar")
        return objRespuesta(
            respuesta = True,
            data=db_provincia
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al actualizar registros: {str(e)}"
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al actualizar registros: {str(e)}"
        )
