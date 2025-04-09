from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.models import Empresa, UsuarioEmpresaRol
from app.schemas.empresa import EmpresaAcceso, EmpresaCreate

def crear_empresa(db: Session, empresa: EmpresaCreate):
    db_empresa = Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

def getDatosEmpresa(db: Session, UsuarioId: int):
    userEmpRolObj = db.query(UsuarioEmpresaRol).filter(
        and_(UsuarioEmpresaRol.id_usuario == UsuarioId, 
             UsuarioEmpresaRol.estado == True)).all()
    if not userEmpRolObj:
        raise Exception("Registro UsuarioRolEmpresa no encontrada ")
    
    empresa_ids = [item.id_empresa for item in userEmpRolObj]
    
    empresaList = db.query(Empresa).filter(Empresa.id.in_(empresa_ids)).all()
    
    if not empresaList:
        raise Exception("Empresas no encontrada")
    
    # Si hay empresas, las convertimos a Pydantic
    empresa_pydantic_list = [EmpresaAcceso.from_orm(empresa) for empresa in empresaList]

    # Si necesitas devolver solo una empresa (por ejemplo, la primera), puedes hacer esto:
    if empresa_pydantic_list:
        return empresa_pydantic_list  # O devolver la lista completa si es necesario
    else:
        return None
  
