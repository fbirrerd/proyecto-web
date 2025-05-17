from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.tipoMenu import MenusOut, TipoMenuCreate, TipoMenuList, TipoMenuOut, TipoMenuUpdate
from app.models.models import Menu, TipoMenu


def get_all(db: Session) ->  list[TipoMenuOut]:
    return db.query(TipoMenu).order_by(TipoMenu.nombre).all()

def get_by_id(db: Session, id: int) ->  TipoMenuOut:
    return db.query(TipoMenu).filter(TipoMenu.id == id).first()
    

def create(db: Session, data: TipoMenuCreate) ->  TipoMenuOut:
    nuevo = TipoMenu(**data.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def update(db: Session, id: int, data: TipoMenuUpdate) -> TipoMenuOut:
    # Buscar el objeto por ID
    obj = db.query(TipoMenu).filter(TipoMenu.id == id).first()

    if not obj:
        raise HTTPException(
            status_code=404,
            detail=f"TipoMenu con id={id} no encontrado."
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

def get_lista(db: Session) ->  TipoMenuOut:
    datos = db.query(TipoMenu).filter(TipoMenu.estado == True).all()
    return [TipoMenuList.from_orm(emp) for emp in datos]

def get_lista_menus_x_tipo(id_tipo_empresa: int,db: Session) ->  MenusOut:
    datos = db.query(Menu).filter(Menu.id_tipo_empresa==id_tipo_empresa).all()
    return [MenusOut.from_orm(emp) for emp in datos]