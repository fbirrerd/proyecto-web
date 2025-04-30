from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db


from crud.email import crear_email
from schemas.email import EmailCreate
from schemas.respond import objRespuesta

router = APIRouter(
    prefix="/email",
    tags=["Emails"]
)

@router.post("/", response_model=objRespuesta)
def create_email(email: EmailCreate, db: Session = Depends(get_db)):
 
    try:

        new_email = crear_email(db, email)
        return objRespuesta(
            respuesta=True,
            data=new_email
        ) 
    except Exception as e:
        print("❌ Error al crear email:", e)
        raise

