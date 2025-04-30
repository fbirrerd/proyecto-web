from sqlalchemy.orm import Session


from app.models.models import EmpresaModulo, Modulo
from app.schemas.modulos import ModuloCreate, ModuloUpdate

def get_modulos(db: Session):
    return db.query(Modulo).all()

def get_modulo(db: Session, modulo_id: int):
    return db.query(Modulo).filter(Modulo.id == modulo_id).first()

def create_modulo(db: Session, modulo: ModuloCreate):
    db_modulo = Modulo(**modulo.dict())
    db.add(db_modulo)
    db.commit()
    db.refresh(db_modulo)
    return db_modulo

def update_modulo(db: Session, modulo_id: int, modulo: ModuloUpdate):
    db_modulo = get_modulo(db, modulo_id)
    if db_modulo:
        for key, value in modulo.dict(exclude_unset=True).items():
            setattr(db_modulo, key, value)
        db.commit()
        db.refresh(db_modulo)
    return db_modulo

def delete_modulo(db: Session, modulo_id: int):
    db_modulo = get_modulo(db, modulo_id)
    if db_modulo:
        db.delete(db_modulo)
        db.commit()
    return db_modulo




def obtener_modulos_por_empresa(db: Session, empresa_id: int):
    # Paso 1: Obtener los id_modulo
    ids_modulos = db.query(EmpresaModulo.id_modulo).filter(EmpresaModulo.id_empresa == empresa_id).all()
    
    # Extraer solo los valores (porque .all() retorna una lista de tuplas)
    lista_ids = [id[0] for id in ids_modulos]

    # Paso 2: Consultar los módulos
    moduloList = db.query(Modulo).filter(Modulo.id.in_(lista_ids)).all()
    
    # if not moduloList:
    #     raise Exception("Empresas no encontrada")
    
    # Si hay empresas, las convertimos a Pydantic
    modulos_pydantic_list = [Modulo.from_orm(mod) for mod in moduloList]

    return modulos_pydantic_list