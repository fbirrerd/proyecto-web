from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.respond import objRespuesta
from app.database import SessionLocal
from app.schemas.empresa import EmpresaCreate, EmpresaOut, EmpresaUpdate
from app.services.empresa import create, delete, get_all, get_by_id, get_lista, get_lista_usuarios, update, update_estado

router = APIRouter(tags=["Empresa"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_empresas(db: Session = Depends(get_db)):
    try:
        empresas = get_all(db)
        return objRespuesta(respuesta = True, data=empresas)
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al obtener registros: {str(e)}"
        )

@router.get("/{empresa_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_empresa(empresa_id: int, db: Session = Depends(get_db)):
    try:
        empresa = get_by_id(db, empresa_id)
        if not empresa:
            return objRespuesta(respuesta = False, data="Empresa no encontrada")
        return objRespuesta(respuesta = True, data=empresa)
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al obtener registros: {str(e)}"
        )

@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def crear_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    try:
        nueva = create(db, empresa)
        return objRespuesta(respuesta = True, data=nueva)
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al crear registro: {str(e)}"
        )

@router.put("/{empresa_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def actualizar_empresa(empresa_id: int, data: EmpresaUpdate, db: Session = Depends(get_db)):
    try:
        actualizada = update(db, empresa_id, data)
        if not actualizada:
            return objRespuesta(respuesta = False, data="Empresa no encontrada")
        return objRespuesta(respuesta = True, data=actualizada)
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al actualizar registro: {str(e)}"
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al actualizar registro: {str(e)}"
        )

@router.put("estado/{empresa_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def actualizar_empresa(empresa_id: int, data: EmpresaUpdate, db: Session = Depends(get_db)):
    try:
        actualizada = update_estado(db, empresa_id, data)
        if not actualizada:
            return objRespuesta(respuesta = False, data="Empresa no encontrada")
        return objRespuesta(respuesta = True, data=actualizada)
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al actualizar registro: {str(e)}"
        )
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al actualizar registro: {str(e)}"
        )

@router.delete("/{empresa_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def eliminar_empresa(empresa_id: int, db: Session = Depends(get_db)):
    try:
        eliminada = delete(db, empresa_id)
        if not eliminada:
            return objRespuesta(respuesta = False, data="Empresa no encontrada")
        return objRespuesta(respuesta = True, data="Empresa eliminada correctamente")
    except Exception as e:
        return objRespuesta(respuesta = False, data=f"Error al eliminar empresa: {str(e)}")

@router.get("/list/all", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_id_nombre_empresas(db: Session = Depends(get_db)):
    try:
        lista = get_lista(db)
        return objRespuesta(respuesta = True, data=lista)
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al obtener registros: {str(e)}"
        )

@router.get("/lista-usuarios-empresa/{empresa_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def obtener_lista_usuarios_x_empresa(empresa_id:int, db: Session = Depends(get_db)):
    try:
        lista = get_lista_usuarios(db, empresa_id)
        return objRespuesta(
            respuesta = True, 
            data=lista
        ) 
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            errorNum=500,
            errorMensaje=f"Error al obtener registros: {str(e)}"
        )
