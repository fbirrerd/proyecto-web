
from typing import List
from app.schemas.rol import RolAcceso, RolCreate, RolList, RolOut, RolUpdate
from app.models.models import Rol, EmpresaUsuarioRol
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from sqlalchemy import and_, or_



  
def get_rol(db: Session, rol_id: int)  -> RolOut:
    return db.query(Rol).filter(Rol.id == rol_id).first()

def get_all(db: Session)  -> List[RolOut]:
    return db.query(Rol).order_by(Rol.nombre).all()

def create_role(db: Session, role: RolCreate)  -> RolOut:
    db_role = Rol(nombre=Rol.nombre, estado=role.estado)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, rol_id: int, role: RolUpdate)  -> RolOut:
    db_role = db.query(Rol).filter(Rol.id == rol_id).first()
    if db_role:
        db_role.nombre = role.nombre
        db_role.estado = role.estado
        db.commit()
        db.refresh(db_role)
    return db_role


def getDatosRol(db: Session, UsuarioId: int, EmpresaId: int):
    userEmpRolList = db.query(EmpresaUsuarioRol).filter(
        and_(EmpresaUsuarioRol.id_usuario == UsuarioId, 
             EmpresaUsuarioRol.id_empresa == EmpresaId,
             EmpresaUsuarioRol.estado == True)
    ).all()
    if not userEmpRolList:
        raise Exception("Registro UsuarioRolEmpresa no encontrada ")
    
    roles_ids = [item.id_rol for item in userEmpRolList]
    
    rolList = db.query(Rol).filter(Rol.id.in_(roles_ids)).all()
    
    if not rolList:
        raise Exception("Roles no encontrados")
    
    # Si hay empresas, las convertimos a Pydantic
    rol_pydantic_list = [RolAcceso.from_orm(empresa) for empresa in rolList]

    # Si necesitas devolver solo una empresa (por ejemplo, la primera), puedes hacer esto:
    if rol_pydantic_list:
        return rol_pydantic_list  # O devolver la lista completa si es necesario
    else:
        return None
    
def get_lista(db: Session) ->  List[RolList]:
    datos = db.query(Rol).filter(Rol.estado == True).all()
    return [RolList.from_orm(r) for r in datos]
