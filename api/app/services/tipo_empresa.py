from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.models import TipoEmpresa
from app.schemas.tipo_empresa import TipoEmpresaCreate, TipoEmpresaList, TipoEmpresaOut, TipoEmpresaUpdate

def get_all(db: Session) ->  list[TipoEmpresaOut]:
    return db.query(TipoEmpresa).order_by(TipoEmpresa.nombre).all()

def get_by_id(db: Session, id: int) ->  TipoEmpresaOut:
    return db.query(TipoEmpresa).filter(TipoEmpresa.id == id).first()
    

def create(db: Session, data: TipoEmpresaCreate) ->  TipoEmpresaOut:
    nuevo = TipoEmpresa(**data.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def update(db: Session, id: int, data: TipoEmpresaUpdate) -> TipoEmpresaOut:
    # Buscar el objeto por ID
    obj = db.query(TipoEmpresa).filter(TipoEmpresa.id == id).first()

    if not obj:
        raise HTTPException(
            status_code=404,
            detail=f"TipoEmpresa con id={id} no encontrado."
        )

    # Filtrar los campos que no sean None y solo los que se enviaron
    update_data = {
        field: value for field, value in data.dict(exclude_unset=True).items()
        if value is not None
    }

    for field, value in update_data.items():
        setattr(obj, field, value)

    try:
        db.commit()
        db.refresh(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar: {str(e)}"
        )

    return obj

def get_lista(db: Session) ->  TipoEmpresaList:
    datos = db.query(TipoEmpresa).filter(TipoEmpresa.estado == True).all()
    return [TipoEmpresaList.from_orm(emp) for emp in datos]