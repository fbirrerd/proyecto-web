from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.tipoMenu import TipoMenuCreate, TipoMenuUpdate
from app.services.tipoMenu import create, get_all, get_lista, get_lista_menus_x_tipo, update
from app.schemas.respond import objRespuesta
from app.database import SessionLocal


router = APIRouter(tags=["TipoMenu"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def listar(db: Session = Depends(get_db)):
    datos = get_all(db=db)
    return  objRespuesta(
        respuesta=True,
        data=datos
    )    

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def crear(data: TipoMenuCreate, db: Session = Depends(get_db)):
    datos = create(db,data)
    return  objRespuesta(
        respuesta=True,
        data=datos
    ) 

@router.put("/{id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def actualizar(id: int, data: TipoMenuUpdate, db: Session = Depends(get_db)):
    result = update(db, id, data)
    if not result:
        raise HTTPException(status_code=404, detail="TipoMenu no encontrado")
    return  objRespuesta(
        respuesta=True,
        data=result
    ) 
@router.get("/list/all", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_id_nombre_empresas(db: Session = Depends(get_db)):
    lista = get_lista(db)
    return objRespuesta(
        respuesta=True,
        data=lista
    )
@router.get("/menus/{id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def get_lista_empresas(id: int, db: Session = Depends(get_db)):
    lista = get_lista_menus_x_tipo(id, db)
    return objRespuesta(
        respuesta=True,
        data=lista
    )