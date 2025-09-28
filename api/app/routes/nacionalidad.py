from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.nacionalidad import NacionalidadCreate, NacionalidadUpdate
from app.schemas.respond import objRespuesta
from app.services.nacionalidad import create, get_all, get_by_id, update
from app.database import SessionLocal

router = APIRouter(tags=["Nacionalidad"])

# Dependency para obtener la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_nacionalidades(db: Session = Depends(get_db)):
    try:
        data = get_all(db=db)
        return objRespuesta(
            respuesta = True, 
            data = data
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum = 500,
            errorMensaje = f"Error al obtener registros: {str(e)}"
        )

@router.get("/{id_nacionalidad}", response_model=objRespuesta, responses={404: {"model": objRespuesta}})
def read_nacionalidad(id_nacionalidad: int, db: Session = Depends(get_db)):
    try:
        data = get_by_id(db, id_nacionalidad)
        if data is None:
            raise HTTPException(status_code=404, detail="Nacionalidad no encontrada")
        return objRespuesta(
            respuesta = True,
            data = data
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la nacionalidad: {str(e)}")

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def set_nacionalidad(nacionalidad: NacionalidadCreate, db: Session = Depends(get_db)):
    try:
        data = create(db, nacionalidad)
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

@router.put("/{modulo_id}", response_model=objRespuesta, responses={404: {"model": objRespuesta}})
def update_nacionalidad(modulo_id: int, obj: NacionalidadUpdate, db: Session = Depends(get_db)):
    try:
        data = update(db, modulo_id, obj)
        if data is None:
            raise HTTPException(status_code=404, detail="Nacionalidad no encontrada para actualizar")
        return objRespuesta(
            respuesta = True,
            data = data
        )
    except Exception as e:
        return objRespuesta(respuesta = False, data=f"Error al actualizar estado: {str(e)}")
