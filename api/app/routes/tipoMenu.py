from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.tipoMenu import TipoMenuCreate, TipoMenuUpdate
from app.services.tipoMenu import (
    create,
    get_all,
    get_lista,
    get_lista_menus_x_tipo,
    update
)
from app.schemas.respond import objRespuesta
from app.database import SessionLocal

router = APIRouter(tags=["TipoMenu"])

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# ENDPOINT: Listar todos los tipos de menú
# -------------------------------
@router.get("/", response_model=objRespuesta)
def read_tipos_menu(db: Session = Depends(get_db)):
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

# -------------------------------
# ENDPOINT: Crear nuevo tipo de menú
# -------------------------------
@router.post("/", response_model=objRespuesta)
def crear_tipo_menu(data: TipoMenuCreate, db: Session = Depends(get_db)):
    try:
        data = create(db, data)
        return objRespuesta(respuesta = True, data = data)
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al crear registro: {str(e)}"
        )

# -------------------------------
# ENDPOINT: Actualizar tipo de menú
# -------------------------------
@router.put("/{id}", response_model=objRespuesta)
def actualizar_tipo_menu(id: int, data: TipoMenuUpdate, db: Session = Depends(get_db)):
    try:
        result = update(db, id, data)
        if not result:
            raise HTTPException(status_code=404, detail="TipoMenu no encontrado")
        return objRespuesta(respuesta = True, data=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar tipo de menú: {str(e)}")

# -------------------------------
# ENDPOINT: Obtener lista ID-Nombre de tipos de menú
# -------------------------------
@router.get("/list/all", response_model=objRespuesta)
def obtener_lista_tipo_menu(db: Session = Depends(get_db)):
    try:
        lista = get_lista(db)
        return objRespuesta(respuesta = True, data=lista)
    except Exception as e:
        return objRespuesta(respuesta = False, mensaje=f"Error al obtener lista: {str(e)}", data=[])

# -------------------------------
# ENDPOINT: Obtener lista de menús por tipo de menú
# -------------------------------
@router.get("/menus/{id}", response_model=objRespuesta)
def obtener_menus_por_tipo(id: int, db: Session = Depends(get_db)):
    try:
        lista = get_lista_menus_x_tipo(id, db)
        return objRespuesta(respuesta = True, data=lista)
    except Exception as e:
        return objRespuesta(respuesta = False, mensaje=f"Error al obtener menús por tipo: {str(e)}", data=[])
