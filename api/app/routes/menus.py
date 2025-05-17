from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.respond import objRespuesta
from app.schemas.menus import MenuEstadoUpdate, MenuUpdate
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
def obtener_menus_generales(db: Session = Depends(get_db)):  
    try:
        data = getListMenuOrdenada(db, None, None)
        return objRespuesta(respuesta=True, data=data)
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al obtener menús: {str(e)}")

@router.put("/generales", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def actualizar_datos_menu(menu: MenuUpdate, db: Session = Depends(get_db)):
    try:
        respuesta = actualizar_menu(db, menu)
        if respuesta:
            return objRespuesta(respuesta=True, data=respuesta)
        return objRespuesta(
            respuesta=False,
            data={"numero": 401, "mensaje": "Problema al actualizar los datos del menú"}
        )
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al actualizar menú: {str(e)}")

@router.put("/cambiar-estado", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def cambiar_estado_menu(menu: MenuEstadoUpdate, db: Session = Depends(get_db)):
    try:
        respuesta = actualizar_estado(db, menu.id, menu.estado)
        if respuesta:
            return objRespuesta(
                respuesta=True,
                data={"actualiza": respuesta}
            )
        return objRespuesta(
            respuesta=False,
            data={"numero": 401, "mensaje": "Problema al actualizar el estado"}
        )
    except Exception as e:
        return objRespuesta(respuesta=False, data=f"Error al cambiar estado del menú: {str(e)}")
