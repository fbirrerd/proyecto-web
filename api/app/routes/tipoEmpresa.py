from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.respond import objRespuesta
from app.schemas.tipo_empresa import TipoEmpresaCreate, TipoEmpresaUpdate
from app.services.tipo_empresa import create, get_all, get_lista, update
from app.database import SessionLocal


router = APIRouter(tags=["TipoEmpresa"])

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
def crear(data: TipoEmpresaCreate, db: Session = Depends(get_db)):
    datos = create(db,data)
    return  objRespuesta(
        respuesta=True,
        data=datos
    ) 

@router.put("/{id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def actualizar(id: int, data: TipoEmpresaUpdate, db: Session = Depends(get_db)):
    result = update(db, id, data)
    if not result:
        raise HTTPException(status_code=404, detail="TipoEmpresa no encontrado")
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