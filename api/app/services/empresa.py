from typing import List
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.models import Empresa, EmpresaUsuario, EmpresaUsuarioRol
from app.schemas.empresa import EmpresaAcceso, EmpresaCreate, EmpresaList, EmpresaOut, EmpresaUpdate


def getDatosEmpresa(db: Session, UsuarioId: int):
    userEmpObj = db.query(EmpresaUsuario).filter(
        and_(EmpresaUsuario.id_usuario == UsuarioId, 
             EmpresaUsuario.estado == True)).all()
    if not userEmpObj:
        raise Exception("Registro EmpresaUsuario no encontrado")
    
    id_empresas = [item.id_empresa for item in userEmpObj]
    
    empresaList = db.query(Empresa).filter(Empresa.id.in_(id_empresas)).all()
    
    if not empresaList:
        raise Exception("Empresas no encontrada")
    
    # Si hay empresas, las convertimos a Pydantic
    empresa_pydantic_list = [EmpresaAcceso.from_orm(empresa) for empresa in empresaList]

    # Si necesitas devolver solo una empresa (por ejemplo, la primera), puedes hacer esto:
    if empresa_pydantic_list:
        return empresa_pydantic_list  # O devolver la lista completa si es necesario
    else:
        return None
  
def get_all(db: Session) ->  List[EmpresaOut]:
    return db.query(Empresa).order_by(Empresa.nombre).all()

def get_by_id(db: Session, empresa_id: int) ->  EmpresaOut:
    return db.query(Empresa).filter(Empresa.id == empresa_id).first()

def create(db: Session, empresa: EmpresaCreate) ->  EmpresaOut:
    nueva = Empresa(**empresa.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def update(db: Session, empresa_id: int, data: EmpresaUpdate) ->  EmpresaOut:
    obj = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, empresa_id: int) ->  EmpresaOut:
    obj = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj

def get_lista(db: Session) ->  EmpresaList:
    datos = db.query(Empresa).filter(Empresa.estado == True).order_by(Empresa.nombre).all()
    return [EmpresaList.from_orm(emp) for emp in datos]