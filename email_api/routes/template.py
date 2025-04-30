from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db



from crud.template import crear_template
from schemas.template import TemplateCreate
from schemas.respond import objRespuesta

router = APIRouter(
    prefix="/template",
    tags=["Emails"]
)

@router.post("/", response_model=objRespuesta)
def create_email(template: TemplateCreate, db: Session = Depends(get_db)):
    return crear_template(db, template)

