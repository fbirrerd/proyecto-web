from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.respond import objRespuesta
from app.schemas.menus import  MenuEstadoUpdate, MenuUpdate
from app.services.menus import actualizar_estado, actualizar_menu, get_lista_menu, getListMenuOrdenada
from app.database import SessionLocal


router = APIRouter(tags=["Menu"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/generales", response_model=objRespuesta)
def getGenerales(db: Session = Depends(get_db)):  
    return objRespuesta(
        respuesta=True,
        data=getListMenuOrdenada(db, None, None)
    )

@router.put("/generales", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def putGenerales(menu: MenuUpdate, db: Session = Depends(get_db)):
    respuesta = actualizar_menu(db, menu)
    if respuesta:
        return respuesta
    # Si las credenciales no coinciden
    return objRespuesta(
        respuesta=False,
        data={"numero":401, "mensaje":"Problema al actualizar los datos del menu"}
    )
 
@router.put("/cambiar-estado", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def putGeneralesEstado(menu: MenuEstadoUpdate, db: Session = Depends(get_db)):
    respuesta = actualizar_estado(db,menu.id, menu.estado)
    if respuesta:
        return objRespuesta(
            respuesta=True,
            data={"actualiza":respuesta}
        )    
    # Si las credenciales no coinciden
    return objRespuesta(
        respuesta=False,
        data={"numero":401, "mensaje":"Problema al actualizar el estado"}
    ) 
    

# @router.get("/generales/tree", response_model=objRespuesta)
# def getGeneralesTree(db: Session = Depends(get_db)):
#     return getListMenuOrdenada(db)


# @router.get("/especificos/all", response_model=Menu)
# def getEspecificos(empresa: EmpresaCreate, db: Session = Depends(get_db)):
#     return crear_empresa(db, empresa)
