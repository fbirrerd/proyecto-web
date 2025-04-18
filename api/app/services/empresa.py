from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.models import Empresa, EmpresaUsuario, EmpresaUsuarioRol
from app.schemas.empresa import EmpresaAcceso, EmpresaCreate

def crear_empresa(db: Session, empresa: EmpresaCreate):
    db_empresa = Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

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
  
