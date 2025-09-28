from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.vademecum import get_vademecum
from app.database import SessionLocal
from app.schemas.respond import objRespuesta

router = APIRouter(tags=["Vademecum"])

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# ENDPOINT: Obtener lista ID-nombre de empresas
# -------------------------------
# @router.get("/lista/vademecum/cache/{id_empresa}", response_model=objRespuesta)
# def obtener_lista_vademecum( id_empresa: int, db: Session = Depends(get_db)):
#     try:
#         lista = get_vademecum_cache(db,id_empresa)
#         return objRespuesta(respuesta = True, data=lista)
#     except Exception as e:
#         return objRespuesta(
#             respuesta = False,
#             mensaje=f"Error al obtener la lista de empresas: {str(e)}",
#             data=[]
#         )


@router.get("/{id_empresa}", response_model=objRespuesta)
def get_medicamentos(id_empresa: int, db: Session = Depends(get_db)): 
    try:
        medicamentos = get_vademecum(db, id_empresa)
        if not medicamentos:
            raise HTTPException(status_code=404, detail="No medicamentos found")
        return objRespuesta(respuesta = True, data=medicamentos)
    except Exception as e:
        return objRespuesta(
            respuesta = False,
            data=f"Error al obtener la lista de empresas: {str(e)}"
        )
