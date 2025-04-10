
from app.schemas.rol import RolAcceso, RolCreate, RolUpdate
from app.models.models import Rol, UsuarioEmpresaRol
from sqlalchemy.orm import Session


from datetime import datetime, timezone
from sqlalchemy import and_, or_
from app.schemas.respond import objRespuesta


def getDatosRol(db: Session, UsuarioId: int, EmpresaId: int):
    userEmpRolList = db.query(UsuarioEmpresaRol).filter(
        and_(UsuarioEmpresaRol.id_usuario == UsuarioId, 
             UsuarioEmpresaRol.id_empresa == EmpresaId,
             UsuarioEmpresaRol.estado == True)
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
  
def get_role(db: Session, role_id: int)  -> objRespuesta:
    return db.query(Rol).filter(Rol.id == role_id).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100)  -> objRespuesta:
    return db.query(Rol).offset(skip).limit(limit).all()

def create_role(db: Session, role: RolCreate)  -> objRespuesta:
    db_role = Rol(nombre=Rol.nombre, estado=role.estado)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role_id: int, role: RolUpdate)  -> objRespuesta:
    db_role = db.query(Rol).filter(Rol.id == role_id).first()
    if db_role:
        db_role.nombre = role.nombre
        db_role.estado = role.estado
        db.commit()
        db.refresh(db_role)
    return db_role