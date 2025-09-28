from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.respond import objRespuesta
from app.schemas.tipoEmpresa import TipoEmpresaCreate, TipoEmpresaFiltro, TipoEmpresaUpdate
from app.services.tipoEmpresa import create, get_all, get_lista, get_lista_empresas_x_tipo, update
from app.database import SessionLocal


router = APIRouter(tags=["TipoEmpresa"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_tipoempresa(db: Session = Depends(get_db)):
    data = get_all(db=db)
    return  objRespuesta(
        respuesta = True,
        data = data
    )    
    try:
        data = get_all(db=db)
        return objRespuesta(
            respuesta = True, 
            data=usuarios
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al obtener registros: {str(e)}"
        )
    

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def crear(data: TipoEmpresaCreate, db: Session = Depends(get_db)):
    try:
        data = create(db,data)
        return  objRespuesta(
            respuesta = True,
            data = data
        ) 
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al crear registro: {str(e)}"
        )
    

@router.put("/{id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def actualizar(id: int, data: TipoEmpresaUpdate, db: Session = Depends(get_db)):
    result = update(db, id, data)
    if not result:
        raise HTTPException(status_code=404, detail="TipoEmpresa no encontrado")
    return  objRespuesta(
        respuesta = True,
        data=result
    ) 
@router.get("/list/all", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_id_nombre_empresas(db: Session = Depends(get_db)):
    lista = get_lista(db)
    return objRespuesta(
        respuesta = True,
        data=lista
    )
@router.get("/empresas/{id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def get_lista_empresas(id: int, db: Session = Depends(get_db)):
    lista = get_lista_empresas_x_tipo(id, db)
    return objRespuesta(
        respuesta = True,
        data=lista
    )