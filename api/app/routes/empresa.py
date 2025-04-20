from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import false, true
from sqlalchemy.orm import Session
from app.schemas.respond import objRespuesta
from app.database import SessionLocal
from app.schemas.empresa import EmpresaCreate, EmpresaOut, EmpresaUpdate
from app.services.empresa import create, delete, get_all, get_by_id, get_lista, update



router = APIRouter(tags=["Empresa"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def listar_empresas(db: Session = Depends(get_db)):
    empresa = get_all(db)
    return objRespuesta(
        respuesta=true,
        data=empresa
    )

@router.get("/{empresa_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = get_by_id(db, empresa_id)
    if not empresa:
        return objRespuesta(
            respuesta=false,
            data=HTTPException(status_code=404, detail="Empresa no encontrada")
        )
    return objRespuesta(
        respuesta=true,
        data=empresa
    )

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def crear_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    crear = create(db, empresa)
    return objRespuesta(
        respuesta=true,
        data=crear
    )    

@router.put("/{empresa_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def actualizar_empresa(empresa_id: int, data: EmpresaUpdate, db: Session = Depends(get_db)):
    actualizada = update(db, empresa_id, data)
    if not actualizada:
        return objRespuesta(
            respuesta=false,
            data=HTTPException(status_code=404, detail="Empresa no encontrada")
        )    
    return objRespuesta(
        respuesta=true,
        data=actualizada
    )
@router.delete("/{empresa_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def eliminar_empresa(empresa_id: int, db: Session = Depends(get_db)):
    eliminada = delete(db, empresa_id)
    if not eliminada:
        return objRespuesta(
            respuesta=false,
            data=HTTPException(status_code=404, detail="Empresa no encontrada")
        )
    return objRespuesta(
        respuesta=true,
        data={"msg": "Eliminada correctamente"}
    )

@router.get("/list/all", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_id_nombre_empresas(db: Session = Depends(get_db)):
    lista = get_lista(db)
    return objRespuesta(
        respuesta=True,
        data=lista
    )