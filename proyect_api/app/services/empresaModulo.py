from sqlalchemy.orm import Session
from models.modulos import EmpresaModulo
from schemas.modulos import EmpresaModuloCreate

def get_empresas_modulo(db: Session):
    return db.query(EmpresaModulo).all()

def get_empresa_modulo(db: Session, id_empresa: int, id_modulo: int):
    return db.query(EmpresaModulo).filter(
        EmpresaModulo.id_empresa == id_empresa,
        EmpresaModulo.id_modulo == id_modulo
    ).first()

def create_empresa_modulo(db: Session, relacion: EmpresaModuloCreate):
    db_rel = EmpresaModulo(**relacion.dict())
    db.add(db_rel)
    db.commit()
    db.refresh(db_rel)
    return db_rel

def delete_empresa_modulo(db: Session, id_empresa: int, id_modulo: int):
    db_rel = get_empresa_modulo(db, id_empresa, id_modulo)
    if db_rel:
        db.delete(db_rel)
        db.commit()
    return db_rel
