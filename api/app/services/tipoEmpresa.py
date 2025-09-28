from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.models import Empresa, TipoEmpresa
from app.schemas.tipoEmpresa import EmpresasOut, TipoEmpresaCreate, TipoEmpresaFiltro, TipoEmpresaList, TipoEmpresaOut, TipoEmpresaUpdate

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
            status_code=500,
            detail=f"Error al actualizar: {str(e)}"
        )

    return obj

def get_lista(db: Session) ->  TipoEmpresaList:
    data = db.query(TipoEmpresa).filter(TipoEmpresa.estado == True).all()
    return [TipoEmpresaList.from_orm(emp) for emp in data]

def get_lista_empresas_x_tipo(id_tipo_empresa: int,db: Session) ->  EmpresasOut:
    data = db.query(Empresa).filter(Empresa.id_tipo_empresa==id_tipo_empresa).all()
    return [EmpresasOut.from_orm(emp) for emp in data]