from typing import Any, List
from fastapi import HTTPException
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session


from app.schemas.menus import MenuFiltroPlus
from app.models.models import EmpresaModulo, Modulo
from app.schemas.modulo import ModuloBase, ModuloConArbol, ModuloCreate,  ModuloUpdate

def get_modulos(db: Session) -> List[ModuloBase]:
    return db.query(Modulo).all()

def get_modulo(db: Session, modulo_id: int) -> ModuloBase:
    return db.query(Modulo).filter(Modulo.id == modulo_id).first()

def create_modulo(db: Session, modulo: ModuloCreate):
    db_modulo = Modulo(**modulo.dict())
    db.add(db_modulo)
    db.commit()
    db.refresh(db_modulo)
    return db_modulo

def update_modulo(db: Session, modulo_id: int, modulo: ModuloUpdate) -> ModuloBase:
    db_modulo = get_modulo(db, modulo_id)
    if db_modulo:
        for key, value in modulo.dict(exclude_unset=True).items():
            setattr(db_modulo, key, value)
        db.commit()
        db.refresh(db_modulo)
    return db_modulo

def delete_modulo(db: Session, modulo_id: int) -> ModuloBase:
    db_modulo = get_modulo(db, modulo_id)
    if db_modulo:
        db.delete(db_modulo)
        db.commit()
    return db_modulo


def obtener_modulos_por_empresa(db: Session, empresa_id: int) -> list[ModuloConArbol]:
    print(f"Obteniendo módulos para la empresa con ID: {empresa_id}")
    try:
        # Paso 1: Obtener los id_modulo de la empresa
        ids_modulos = db.query(EmpresaModulo.id_modulo).filter(
            and_(
                EmpresaModulo.id_empresa == empresa_id,
                EmpresaModulo.fecha_inicio <= func.now(),
                or_(
                    EmpresaModulo.fecha_fin == None,
                    EmpresaModulo.fecha_fin >= func.now()
                ),
                EmpresaModulo.estado == True
            )
        ).all()
        lista_ids = [id_tuple[0] for id_tuple in ids_modulos]

        if not ids_modulos:
            print(f"No se encontraron módulos asociados a la empresa con ID: {empresa_id}")
            return []

        # Paso 2: Consultar los módulos con esos IDs
        modulos = db.query(Modulo).filter(Modulo.id.in_(lista_ids)).all()

        if not modulos:
            print(f"No se encontraron módulos con los IDs: {lista_ids}")
            raise HTTPException(status_code=404, detail="No se encontraron módulos asociados.")

        # Convertimos a esquema Pydantic (si tienes un schema definido)
        modulos_pydantic = [ModuloConArbol.from_orm(mod) for mod in modulos]

        return modulos_pydantic

    except HTTPException as http_exc:
        print(f"Error HTTP: {http_exc.detail}")
        raise http_exc  
    except Exception as e:
        # Otros errores no controlados
        print(f"Error inesperado al obtener módulos para la empresa {empresa_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {str(e)}")
