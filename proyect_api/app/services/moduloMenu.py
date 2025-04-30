from sqlalchemy.orm import Session
from models.modulos import ModuloMenu
from schemas.modulos import ModuloMenuCreate

def get_modulo_menu(db: Session):
    return db.query(ModuloMenu).all()

def get_relacion(db: Session, id_modulo: int, id_menu: int):
    return db.query(ModuloMenu).filter(
        ModuloMenu.id_modulo == id_modulo,
        ModuloMenu.id_menu == id_menu
    ).first()

def create_modulo_menu(db: Session, relacion: ModuloMenuCreate):
    db_rel = ModuloMenu(**relacion.dict())
    db.add(db_rel)
    db.commit()
    db.refresh(db_rel)
    return db_rel

def delete_modulo_menu(db: Session, id_modulo: int, id_menu: int):
    db_rel = get_relacion(db, id_modulo, id_menu)
    if db_rel:
        db.delete(db_rel)
        db.commit()
    return db_rel
