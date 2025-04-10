from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.rol import RolCreate, RolUpdate
from app.schemas.respond import objRespuesta
from app.services.rol import get_role, get_roles
from app.database import SessionLocal


router = APIRouter(tags=["Rol"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def create_role(role: RolCreate, db: Session = Depends(get_db)):
    return create_role(db=db, role=role)

@router.get("/", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    datos = get_roles(db=db, skip=skip, limit=limit)
    return  objRespuesta(
        respuesta=True,
        data=datos
    )    


@router.get("/{role_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def read_role(role_id: int, db: Session = Depends(get_db)):
    db_role = get_role(db=db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.put("/role_id}", response_model=objRespuesta, responses={400: {"model": objRespuesta}})
def update_role(role_id: int, role: RolUpdate, db: Session = Depends(get_db)):
    db_role = update_role(db=db, role_id=role_id, role=role)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role