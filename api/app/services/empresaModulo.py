from typing import List
from sqlalchemy import func, true
from sqlalchemy.orm import Session

from app.models.models import EmpresaModulo
from app.schemas.empresaModulo import EmpresaModuloCreate, EmpresaModuloOut, EmpresaModuloRelacion, EmpresaModuloUpdate


def get_empresas_modulo(db: Session) -> list[EmpresaModuloOut]:
    return db.query(EmpresaModulo).all()

def get_empresa_modulo(db: Session, id_empresa: int, id_modulo: int)  -> EmpresaModuloOut:
    return db.query(EmpresaModulo).filter(
        EmpresaModulo.id_empresa == id_empresa,
        EmpresaModulo.id_modulo == id_modulo
    ).first()

def create_empresa_modulo(db: Session, relacion: EmpresaModuloCreate)  -> EmpresaModuloOut:
    db_rel = EmpresaModulo(**relacion.dict())
    db.add(db_rel)
    db.commit()
    db.refresh(db_rel)
    return db_rel

def update_empresa_modulo(db: Session, usuario_id: int, data: EmpresaModuloUpdate) ->  EmpresaModuloOut:
    db_empresa_modulo = db.query(EmpresaModulo).filter(EmpresaModulo.id == usuario_id).first()
    if db_empresa_modulo:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(db_empresa_modulo, key, value)
        db.commit()
        db.refresh(db_empresa_modulo)
    return db_empresa_modulo

def delete_empresa_modulo(db: Session, id_empresa: int, id_modulo: int)  -> EmpresaModuloOut:
    db_rel = get_empresa_modulo(db, id_empresa, id_modulo)
    if db_rel:
        db.delete(db_rel)
        db.commit()
    return db_rel

def get_empresas_modulo_X_empresa(db: Session, id_empresa: int) -> list[EmpresaModuloOut]:
    return db.query(EmpresaModulo).filter(
        EmpresaModulo.id_empresa == id_empresa).all()

def create_relacion_empresa_modulo(db: Session, relacion: EmpresaModuloRelacion)  -> EmpresaModuloOut:
    try:
        for modulo in relacion.modulos:
            existente = db.query(EmpresaModulo).filter_by(
                id_empresa=relacion.id_empresa,
                id_modulo=modulo.id_modulo
            ).first()

            if existente:
                # Si ya existe, actualiza el estado
                existente.estado = modulo.estado
            else:
                # Si no existe, crea uno nuevo
                newobj = EmpresaModulo(
                    id_empresa=relacion.id_empresa,
                    id_modulo=modulo.id_modulo,
                    estado=modulo.estado,
                    fecha_inicio=func.now()
                )
                db.add(newobj)
        db.commit()
        return true
    except Exception as e:
        db.rollback()
        raise Exception(f"Error al insertar o actualizar: {str(e)}")

