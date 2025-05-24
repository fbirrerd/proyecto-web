from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.schemas.nacionalidad import NacionalidadCreate, NacionalidadUpdate
from app.schemas.respond import objRespuesta
from app.services.nacionalidad import create, get_all, get_by_id, update
from app.database import SessionLocal


router = APIRouter(tags=["Nacionalidad"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_nacionalidades(db: Session = Depends(get_db)):
    datos = get_all(db)
    return  objRespuesta(
        respuesta=True,
        data=datos
    )    


@router.get("/{id_nacionalidad}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_nacionalidad(id_nacionalidad: int, db: Session = Depends(get_db)):
    datos = get_by_id(db, id_nacionalidad)
    if datos is None:
        raise HTTPException(status_code=404, detail="nacionalidade not found")
    return datos

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def set_nacionalidad(nacionalidad: NacionalidadCreate, db: Session = Depends(get_db)):
    datos = create(db,nacionalidad)
    return  objRespuesta(
        respuesta=True,
        data=datos
    )  
@router.put("/{modulo_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def update_nacionalidad(modulo_id: int, obj: NacionalidadUpdate, db: Session = Depends(get_db)):
    datos = update(db, modulo_id, obj)
    if datos is None:
        raise HTTPException(status_code=404, detail="nacionalidade not found")
    return datos