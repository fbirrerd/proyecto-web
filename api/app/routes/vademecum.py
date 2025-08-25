from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.respond import objRespuesta
from app.services.views import get_vademecum

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
#         return objRespuesta(respuesta=True, data=lista)
#     except Exception as e:
#         return objRespuesta(
#             respuesta=False,
#             mensaje=f"Error al obtener la lista de empresas: {str(e)}",
#             data=[]
#         )

@router.get("/{id_empresa}", response_model=objRespuesta)
def obtener_lista_vademecum(id_empresa: int, db: Session = Depends(get_db)):

    try:
        medicamentos = get_vademecum(db, id_empresa)
        if not medicamentos:
            raise HTTPException(status_code=404, detail="No medicamentos found")
        return medicamentos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving medicamentos: {str(e)}")
